import requests
import httplib
import json

youtube_api_url = 'https://www.googleapis.com/youtube/v3/search?id=7lCDEYXw3mM&key=AIzaSyBNUAfQhQwn07Q8ge6mpiUTodLV6av6z8U&part=snippet&type=video&videoCaption=closedCaption&videoEmbeddable=true&maxResults=1&q='

def get_youtube_video(search_query):
	try:
		resp = requests.get(youtube_api_url+search_query)
		if resp.ok:
			json_resp = json.loads(resp.content)
			return json_resp['items'][0]['id']['videoId']
		else:
			print 'response is not ok', resp
			return None
	except Exception, e:
		print 'Exception occured in get_youtube_video', e
		return None