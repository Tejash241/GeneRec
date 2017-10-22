from imdb import IMDb
import genomelink
import requests
import httplib
import json


def get_movie_details(movie_title):
    ans = None
    try:
        ia = IMDb()
        s_result = ia.search_movie(movie_title)[0]
        ia.update(s_result)

        ans = s_result['cover url']
    except Exception, e:
        aa = 1
    return ans


def get_auth_url():
    authorize_url = genomelink.OAuth.authorize_url(client_id='KyoEsiyBMGDj78a0H197DOA53T9013K8m3zrYs4a',
                                                   callback_url='http://127.0.0.1:8000/app/callback', scope=[
            'report:agreeableness report:neuroticism report:extraversion report:conscientiousness report:openness report:gambling report:anger report:reward-dependence report:harm-avoidance report:novelty-seeking'])

    return authorize_url


youtube_api_url = 'https://www.googleapis.com/books/v1/volumes?key=AIzaSyBNUAfQhQwn07Q8ge6mpiUTodLV6av6z8U&q=isbn%3A+'


def get_google_book(search_query):
    print search_query
    try:
        resp = requests.get(youtube_api_url + search_query)
        print youtube_api_url + search_query
        if resp.ok:
            json_resp = json.loads(resp.content)
            return json_resp['items'][0]['volumeInfo']['previewLink']
        else:
            print 'response is not ok', resp
            return None
    except Exception, e:
        print 'Exception occured in get_google_book', e
        return None
