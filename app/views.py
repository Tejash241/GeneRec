from __future__ import unicode_literals
from django.shortcuts import render
from app.models import UserProfile
from os.path import join
import csv
from sdhacks.settings import BASE_DIR

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

headers = []
with open(join(BASE_DIR, 'get_data', 'phenotypes_scores.csv'), 'r') as csvfile:
	reader = csv.reader(csvfile)
	for row_id, row in enumerate(reader):
		if row_id==0:
			headers = format_headers(row)
		else:
			this_row = format_row(row)
			data_dict = dict(zip(headers, this_row))
			UserProfile.objects.create(cluster_name=None, **data_dict)
