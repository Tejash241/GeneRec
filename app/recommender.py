import db_read_write as dbrw
import numpy as np
import random

THRESHOLD = 0.7
K = 4
PERSONA_TRAITS = ['user_id', 'agreeableness', 'neuroticism', 'extraversion', 'conscientiousness', 'openness', 'anger', 'reward_dependence', 'harm_avoidance', 'gambling', 'novelty_seeking']
"""
Assumes similar features are passed in the exact same order
"""
def get_distance(user1, user2):
	return np.sqrt(np.sum(np.power(np.array(user1)-np.array(user2), 2)))

def clean(vector1, vector2):
	vec1 = []
	vec2 = []
	for i in range(len(vector1)):
		if type(vector1[i])==unicode and type(vector2[i])==unicode:
			continue
		elif vector1[i] is None and vector2[i] is None:
			continue
		else:
			vec1.append(vector1[i])
			vec2.append(vector2[i])			

	return vec1, vec2

def k_medoid_clustering(k, medoids, users):
	clusters = [[]]*k
	for x in range(k):
		clusters[x] = []

	for i in range(k):
		clusters[i].append(medoids[i])

	entropy = [0]*k
	for i in range(len(users)):
		min_distance = np.infty
		cluster_id = -1
		for j in range(k):
			vec1, vec2 = clean(users[i].values(), medoids[j].values())
			dist = get_distance(vec1, vec2)
			if dist < min_distance:
				min_distance = dist
				cluster_id = j

		entropy[cluster_id] += min_distance
		clusters[cluster_id].append(users[i])

	return clusters, np.mean(np.sum(entropy, axis=0))

def cluster_all_users():
	global MEDOIDS
	user_list = dbrw.get_all_users()
	user_personality = []
	for user in user_list:
		new_user = {}
		for col in user:
			if col in PERSONA_TRAITS:
				new_user[col] = user[col]
		user_personality.append(new_user)

	medoids = []
	min_entropy = np.infty
	best_clusters = []
	for trial in range(10):
		while len(medoids)<K:
			medoid_user = random.choice(user_personality)
			medoids.append(medoid_user)
			user_personality.remove(medoid_user)

		clusters, entropy = k_medoid_clustering(K, medoids, user_personality)
		if entropy<min_entropy:
			dbrw.populate_medoids(medoids)
			min_entropy = entropy
			best_clusters = clusters

	dbrw.assign_clusters(best_clusters)

def assign_cluster_to_newuser(user):
	user = user.__dict__
	new_user = {}
	medoids = dbrw.get_all_medoids()
	for col in user:
		if col in PERSONA_TRAITS:
			if user[col] is None:
				user[col] = random.choice(range(1,6))
			new_user[col] = user[col]

	min_distance = np.infty
	best_cluster = None
	print medoids
	for cluster_id in range(K):
		medoid = dbrw.get_single_user(medoids[cluster_id]['user_id'])
		medoid_user = {}
		for col in medoid:
			if col in PERSONA_TRAITS:
				medoid_user[col] = medoid[col]

		vec1, vec2 = clean(new_user.values(), medoid_user.values())
		dist = get_distance(vec1, vec2)
		if dist < min_distance:
			min_distance = dist
			best_cluster = cluster_id

	dbrw.update_user_cluster(new_user['user_id'], str(best_cluster))
	print 'Assigned new user to cluster', best_cluster
