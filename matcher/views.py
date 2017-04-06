#-*- coding: utf-8 -*-
from collections import defaultdict

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
import json
from matcher.constants import HEROES_LIST,HEROES_LIST_FORMATED, COUNTRY_FORMAT, COUNTRY_FORMAT_NAME
from twitter.settings import *
import operator


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #context['result_query'] = get_tweets_from_mongo()
        #save_tweets_to_mongo(HEROES_LIST, collection_mongo_main, 20000)
        #get_tweet_ratio()
        return context


def save_tweets_to_mongo(query, mongo_collection, count):
    searched_tweets = []
    last_id = -1
    max_tweets = count

    error = False
    while len(searched_tweets) < max_tweets:
        try:
            new_tweets = api_twitter.search(q=query, count=count, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            error = True
            print "Error GENERAL"
            print e
            break
    if error:
        print "ERROR LEN: " + str(len(searched_tweets))
    print "Insert"
    mongo_collection.insert_many([tweet._json for tweet in searched_tweets])


@csrf_exempt
def get_popular_heroes(request):
    if request.method == "POST":
        result = {}
        for hero in HEROES_LIST_FORMATED:
            result[hero] = collection_mongo_main.find({'text': {'$regex': hero, '$options': 'i'}}).count()

        sorted_hero = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
        response_data = dict((x, y) for x, y in sorted_hero)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

@csrf_exempt
def get_support_heroes(request):

    opinions_list = defaultdict(dict)
    opinions_list['comic']['TOTAL'] = 0
    opinions_list['movie']['TOTAL'] = 0
    for hero in HEROES_LIST_FORMATED:
        for support in ['comic', 'movie']:
            result = collection_mongo_main.find({'$and': [{'text': {'$regex': hero, '$options': 'i'}}, {'text': {'$regex': support, '$options': 'i'}}]}).count()
            opinions_list[support][hero] = result
            opinions_list[support]['TOTAL'] += result
    return HttpResponse(
        json.dumps(opinions_list),
        content_type="application/json"
    )


@csrf_exempt
def get_countries_heroes(request):
    if request.method == "POST":
        countries_heroes = list(collection_mongo_main.aggregate([{'$group': {'_id': '$user.lang', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 20}]))
        countries_heroes_list = {}
        for country in countries_heroes:
            real_country = COUNTRY_FORMAT[country['_id']]
            countries_heroes_list[real_country] = country['count']

        return HttpResponse(
            json.dumps(countries_heroes_list),
            content_type="application/json"
        )


@csrf_exempt
def get_fav_heroes_by_country(request):
    countries_list = get_countries()
    countries_heroes = defaultdict(dict)
    for country in countries_list:
        for hero in HEROES_LIST_FORMATED:
            result = collection_mongo_main.find({'$and': [{'text': {'$regex': hero, '$options': 'i'}},{'user.lang': country['_id']}]}).count()
            countries_heroes[COUNTRY_FORMAT_NAME[country['_id']]][hero] = result
            countries_heroes['HEROES'][hero] = hero
    return HttpResponse(
        json.dumps(countries_heroes),
        content_type="application/json"
    )


@csrf_exempt
def get_tweet_ratio(request):
    if request.method == "POST":
        total = collection_mongo_main.find().count()

        part = 0
        for hero in HEROES_LIST_FORMATED:
            part += collection_mongo_main.find({'text': {'$regex': hero, '$options': 'i'}}).count()

        response_data = {'name_part': total-part, 'text_part':part}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

@csrf_exempt
def get_support_heroes_by_hero(request):

    opinions_list = defaultdict(dict)

    for support in ['comic', 'movie']:
        for hero in HEROES_LIST_FORMATED:
            result = collection_mongo_main.find({'$and': [{'text': {'$regex': hero, '$options': 'i'}}, {'text': {'$regex': support, '$options': 'i'}}]}).count()
            opinions_list[hero][support] = result
            if 'TOTAL' in opinions_list[hero]:
                opinions_list[hero]['TOTAL'] += result
            else:
                opinions_list[hero]['TOTAL'] = result

    return HttpResponse(
        json.dumps(opinions_list),
        content_type="application/json"
    )


def get_countries():
    countries_heroes = collection_mongo_main.aggregate([{'$group': {'_id': '$user.lang', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 20}])
    return list(countries_heroes)