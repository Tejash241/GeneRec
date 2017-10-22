from imdb import IMDb
import genomelink


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
