#-*- coding: utf-8 -*-
from django.views.generic import TemplateView
from twitter.settings import *


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['result_query'] = get_tweets_from_mongo()
        return context


def save_tweets_to_mongo():
    searched_tweets = []
    last_id = -1
    max_tweets = 14000
    query = 'BATMAN OR SPIDERMAN OR SUPERMAN'
    while len(searched_tweets) < max_tweets:
        try:
            new_tweets = api_twitter.search(q=query, count=1000, max_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            print e
            break
    collection_mongo.insert_many([tweet._json for tweet in searched_tweets])


def get_tweets_from_mongo():
    result = collection_mongo.find({}).limit(50)
    return result
