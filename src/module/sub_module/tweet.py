from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys
from abc import ABCMeta, abstractmethod
import numpy as np


class TweetsGetter(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.session = OAuth1Session(CK, CS, AT, AS)

    @abstractmethod
    def specifyUrlAndParams(self, keyword):

    @abstractmethod
    def pickupTweet(self, res_text, includeRetweet):

    @abstractmethod
    def getLimitContext(self, res_text):
        self.checkLimit()

        url, params = self.specifyUrlAndParams()
        params['include_rts'] = str(includeRetweet).lower()
        cnt = 0
        unavailableCnt = 0
        while True:
            res = self.session.get(url, params = params)
            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)

                unavailableCnt += 1
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)

            tweets = self.pickupTweet(json.loads(res.text))
            if len(tweets) == 0:
                break

            for tweet in tweets:
                if (('retweeted_status' in tweet) and (includeRetweet is False)):
                    pass
                else:
                    if onlyText is True:
                        yield tweet['text']
                    else:
                        yield tweet

                    cnt += 1

                    if total > 0 and cnt >= total:
                        return

            params['max_id'] = tweet['id'] - 1

            if ('X-Rate-Limit-Remaining' in res.headers and 'X-Rate-Limit-Reset' in res.headers):
                if (int(res.headers['X-Rate-Limit-Remaining']) == 0):
                    self.waitUntilReset(int(res.headers['X-Rate-Limit-Reset']))
                    self.checkLimit()
            else:
                self.checkLimit()

    def checkLimit(self):
        unavailableCnt = 0
        while True:
            # url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
            res = self.session.get(url)

            if res.status_code == 503:
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)

                unavailableCnt += 1
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
                continue

            unavailableCnt = 0

            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)

            remaining, reset = self.getLimitContext(json.loads(res.text))
            if (remaining == 0):
                self.waitUntilReset(reset)
            else:
                break

    def waitUntilReset(self, reset):
        seconds = reset - time.mktime(datetime.datetime.now().timetuple())
        seconds = max(seconds, 0)
        sys.stdout.flush()

    @staticmethod
    def bySearch(keyword):
        return TweetsGetterBySearch(keyword)

    @staticmethod
    def byUser(screen_name):
        return TweetsGetterByUser(screen_name)


class TweetsGetterBySearch(TweetsGetter):
    def __init__(self, keyword):
        super(TweetsGetterBySearch, self).__init__()
        self.keyword = keyword

    def specifyUrlAndParams(self):
        url = 'https://api.twitter.com/1.1/search/tweets.json'
        params = {'q':self.keyword, 'count':100}
        return url, params

    def pickupTweet(self, res_text):
        results = []
        for tweet in res_text['statuses']:
            results.append(tweet)
        return results
