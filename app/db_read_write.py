from app.models import *
from sdhacks.settings import BASE_DIR
from os.path import join
import csv
import json
import random
from django.db.models import Q

def get_all_users():
	return list(UserProfile.objects.values())

def get_single_user(user_id):
	return UserProfile.objects.get(user_id=user_id).__dict__

def update_user_cluster(user_id, cluster_name):
	user = UserProfile.objects.get(user_id=user_id)
	user.cluster_name = cluster_name
	user.save()
	# UserProfile.objects.update(**dict(zip(field_name, value)))

def get_physical_traits(user_id):
	traits = ['eye_color', 'beard_thickness', 'morning_person', 'weight', 'bmi', 'red_hair', 'black_hair', 'motion_sickness', 'lobe_size', 'handedness', 'longevity', 'skin_pigmentation', 'male_pattern_baldness_aga', 'freckles']
	user = get_single_user(user_id)
	user_traits = [user[t] for t in traits]
	return user_traits

def get_personality_traits(user_id):
	personas = ['agreeableness', 'neuroticism', 'extraversion', 'conscientiousness', 'openness', 'depression', 'anger', 'reward_dependence', 'harm_avoidance', 'gambling', 'novelty_seeking'] 
	user = get_single_user(user_id)
	user_personas = [user[p] for p in personas]
	return user_personas


def format_headers(row):
	headers = []
	headers.append('user_id')
	for header in row[1:]:
		headers.append(header.replace('-', '_'))

	return headers

def format_row(row):
	fr = []
	fr.append(row[0])
	for val in row[1:]:
		if val=='':
			fr.append(None)
		else:
			fr.append(int(val))
	return fr

def populate_users_from_csv(csv_file):
	headers = []
	with open(csv_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row_id, row in enumerate(reader):
			if row_id==0:
				headers = format_headers(row)
			else:
				this_row = format_row(row)
				data_dict = dict(zip(headers, this_row))
				UserProfile.objects.create(cluster_name=None, **data_dict)


def assign_clusters(clusters):
	for i in range(len(clusters)):
		for x in range(len(clusters[i])):
			update_user_cluster(clusters[i][x]['user_id'], str(i))


def format_headers_movies(row):
	headers = []
	for val in row:
		if val == 'id':
			headers.append('movie_id')
		elif val in ['budget', 'genres', 'homepage', 'title', 'overview', 'production_companies', 'release_date', 'tagline', 'vote_average', 'spoken_languages']:
			headers.append(val)
	print headers
	return headers

def format_row_movies(row):
	fr = []
	valid_i = [0,1,2,3,7,9,11,14,16,17,18]
	for i, val in enumerate(row):
		if i==1:
			val = json.loads(val)
			this_genre = ''
			for genre in val:
				this_genre += genre['name']+', '

			this_genre = this_genre[:-2]
			fr.append(this_genre)
		elif i==9:
			val = json.loads(val)
			this_comp = ''
			for comp in val:
				this_comp += comp['name']+', '

			this_comp = this_comp[:-2]
			fr.append(this_comp)
		elif i==14:
			val = json.loads(val)
			this_lang = ''
			for lang in val:
				this_lang += lang['name']+', '

			this_lang = this_lang[:-2]
			fr.append(this_lang)
		elif i in valid_i:
			fr.append(val)

	return fr

def populate_movies_from_csv(csv_file):
	headers = []
	with open(csv_file, 'r') as csvfile:
		reader = csv.reader(csvfile)
		for row_id, row in enumerate(reader):
			if row_id==0:
				headers = format_headers_movies(row)
			else:
				this_row = format_row_movies(row)
				data_dict = dict(zip(headers, this_row))
				Movie.objects.create(**data_dict)

def populate_movies_map():
	user_qs = list(UserProfile.objects.filter(conscientiousness__gt=1, openness__gt=1))
	movie_qs = list(Movie.objects.filter(Q(genres__icontains='Drama')|Q(genres__icontains='Comedy')))
	for u in range(20):
		user = random.choice(user_qs)
		for m in range(30):
			movie = random.choice(movie_qs)
			data_dict = {'user':user, 'movie':movie, 'rating':random.choice([3,4,5])}
			UserMovieMap.objects.create(**data_dict)
	
	user_qs = list(UserProfile.objects.filter(anger__gt=2, extraversion__gt=1))
	movie_qs = list(Movie.objects.filter(Q(genres__icontains='Crime')|Q(genres__icontains='Action')))
	for u in range(4):
		user = random.choice(user_qs)
		for m in range(50):
			movie = random.choice(movie_qs)
			data_dict = {'user':user, 'movie':movie, 'rating':random.choice([3,4,5])}
			UserMovieMap.objects.create(**data_dict)		

	user_qs = list(UserProfile.objects.filter(agreeableness__gt=1, novelty_seeking__gt=3))
	movie_qs = list(Movie.objects.filter(Q(genres__icontains='Thriller')|Q(genres__icontains='Fantasy')|Q(genres__icontains='Science Fiction')))
	for u in range(10):
		user = random.choice(user_qs)
		for m in range(60):
			movie = random.choice(movie_qs)
			data_dict = {'user':user, 'movie':movie, 'rating':random.choice([3,4,5])}
			UserMovieMap.objects.create(**data_dict)

def populate_medoids(medoids):
	UserMedoids.objects.all().delete()
	for i, med in enumerate(medoids):
		UserMedoids.objects.create(**{'cluster_name':str(i), 'user_id':med['user_id']})

def get_all_medoids():
	return list(UserMedoids.objects.values())


def populate_songs_from_txt(txt_file):
	line_counter = 0
	with open(txt_file, 'r') as txtfile:
		for line in txtfile:
			id1, id2, artist, name = line.split('<SEP>')
			Song.objects.create(**{'name':name, 'artist':artist})
			line_counter += 1
			if line_counter > 10000:
				break

def populate_songs_map():
	user_qs = list(UserProfile.objects.filter(anger__gt=3, extraversion__gt=2))
	song_qs = list(Song.objects.filter(Q(name__icontains='Punk')|Q(name__icontains='Rock')|Q(name__icontains='Death')))
	for u in range(len(user_qs)):
		for s in range(40):
			song = random.choice(song_qs)
			data_dict = {'user':user_qs[u], 'song':song, 'rating':random.choice([3,4,5])}
			UserSongMap.objects.create(**data_dict)

	user_qs = list(UserProfile.objects.filter(agreeableness__gt=2, novelty_seeking__gt=2))
	song_qs = list(Song.objects.filter(Q(name__icontains='Calm')|Q(name__icontains='Love')|Q(name__icontains='Sleep'))) 
	for u in range(len(user_qs)):
		for s in range(50):
			song = random.choice(song_qs)
			data_dict = {'user':user_qs[u], 'song':song, 'rating':random.choice([3,4,5])}
			UserSongMap.objects.create(**data_dict)

	user_qs = list(UserProfile.objects.filter(conscientiousness__gt=3))
	song_qs = list(Song.objects.filter(Q(name__icontains='Life')|Q(name__icontains='Goal'))) 
	for u in range(len(user_qs)):
		for s in range(25):
			song = random.choice(song_qs)
			data_dict = {'user':user_qs[u], 'song':song, 'rating':random.choice([3,4,5])}
			UserSongMap.objects.create(**data_dict)	