#-*- coding: utf-8 -*-
from collections import defaultdict

from django.views.generic import TemplateView

from matcher.constants import HEROES_LIST,HEROES_LIST_FORMATED
from twitter.settings import *
import operator

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        #context['result_query'] = get_tweets_from_mongo()
        #save_tweets_to_mongo(HEROES_LIST, collection_mongo_main, 20000)
        get_tweet_ratio()
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


def get_popular_heroes():
    result = {}
    for hero in HEROES_LIST_FORMATED:
        result[hero] = collection_mongo_main.find({'text': {'$regex': hero, '$options': 'i'}}).count()

    sorted_hero = sorted(result.items(), key=operator.itemgetter(1), reverse=True)

    return sorted_hero


def get_good_opinion_heroes():

    opinions_list = defaultdict(dict)

    for hero in HEROES_LIST_FORMATED:
        for support in ['comic', 'movie']:
            result = collection_mongo_main.find({'$and': [{'text': {'$regex': hero, '$options': 'i'}}, {'text': {'$regex': support, '$options': 'i'}}]}).count()
            opinions_list[support][hero] = result
    return opinions_list


def get_countries_heroes():

    countries_heroes = collection_mongo_main.aggregate([{'$group': {'_id': '$user.lang', 'count': {'$sum': 1}}}, {'$sort': {'count': -1}}, {'$limit': 20}])

    return list(countries_heroes)


def get_fav_heroes_by_country():
    countries_list = get_countries_heroes()
    countries_heroes = defaultdict(dict)
    for country in countries_list:
        for hero in HEROES_LIST_FORMATED:
            result = collection_mongo_main.find({'$and': [{'text': {'$regex': hero, '$options': 'i'}},{'user.lang': country['_id']}]}).count()
            countries_heroes[country['_id']][hero] = result
    return countries_heroes


def get_tweet_ratio():
    total = collection_mongo_main.find().count()

    part = 0
    for hero in HEROES_LIST_FORMATED:
        part += collection_mongo_main.find({'text': {'$regex': hero, '$options': 'i'}}).count()

    return total, part
