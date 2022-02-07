#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from urllib.request import urlopen
import math
import os
from pathlib import Path
import csv
import time
import sys


# --------- INIT ----------
# lists
park_name = []
park_id = []
percent = []
merged_list_ParkName = []
merged_list_percent = []
cleaned_percent = []
CSV_HEADER = [
    'DATETIME',
    'Bahnhofsgarage',
    'Konzerthaus',
    'Volksbank',
    'Am Bahnhof',
    'Zur Unterführung',
    'G.-Graf-Halle',
    'Unterlinden',
    'Schwarzwald City',
    'Rotteck',
    'Zähringer Tor',
    'Karlsbau',
    'Landratsamt',
    'Schlossberg',
    'Schwabentor',
    'Martinstor',
    'Kollegiengebäude',
    'Päd. Hochschule',
    'Zentrum Oberwiehre',
    'Westarkaden',
    'Messe Parkplatz'
]

# --------- CONFIG ----------
# path
# datapath = 'data/fr_park/'  # relative path for local testing
datapath = '/scraper/data/fr_park/'  # absolute path for docker-linux
path = datapath + 'fr_park.csv'

try:
    Path(datapath).mkdir(parents=True, exist_ok=True)  # if folders don't exist
    Path(path).touch(exist_ok=True)  # if csv don't exists
except PermissionError:
    print('Creating folder and csv-file failed. Check permissions.')
    sys.exit()

# write zeros if file is empty
csv_empty = os.stat(path).st_size == 0

if csv_empty is True:
    with open(path, 'w', encoding='utf8', newline='') as f:
        writeZero = csv.writer(f)
        writeZero.writerow(CSV_HEADER)


# --------- SCRAPER ----------
time.sleep(5)  # time offset, so the scraper doesn't grab old data from the origin

with urlopen("https://geoportal.freiburg.de/viewer/pls/geojson.php") as url:
    s = url.read()
    encoding = url.headers.get_content_charset('utf-8')
    data = s.decode(encoding)
    data = json.loads(data)
    # print(data)


print('############## OUTPUT ##############')


# timestamp
timestamp = [data['features'][0]['properties']['obs_ts']]
TS = data['features'][0]['properties']['obs_ts']


# park name
for x in range(len(data['features'])):
    park_name.append(data['features'][x]['properties']['park_name'])


# park ID
for x in range(len(data['features'])):
    park_id.append(int(data['features'][x]['properties']['park_id'][1:]))


# percent
for x in range(len(data['features'])):
    try:
        obs_max = int(data['features'][x]['properties']['obs_max'])
        obs_free = int(data['features'][x]['properties']['obs_free'])
        flip = math.floor((obs_max-obs_free)/(obs_max/100))
        percent.append(str(flip))

    except ZeroDivisionError:
        if obs_max == 0:
            percent.append('0')
            print('[1] WARNING: Error in index: ' + str(x) + '. Maximum occupancy equals zero, writing 0 into '
                                                                  'list.')
        else:
            print('[1] ERROR: Division Error in index nr: ' + str(x) + '. REMOVED index from all lists')
            park_name.pop(x)
        pass


# Debug lists // check if length of lists are equal
if len(park_id) == len(park_name):
    print('[2] (Check Lists): Lists are equal.\n')
else:
    print('[2] (Check Lists) WARNING: Lists are NOT matching!\n')


# merge lists and sort it. because the origin messes the order for some reason
# # Merged and sorted park_name-list
# for i in range(len(park_id)):
#     merged_list_ParkName.append([park_id[i], park_name[i]])
#
# sorted_list_ParkName = sorted(merged_list_ParkName)

# Merged and sorted percent-list
for i in range(len(park_id)):
    merged_list_percent.append([park_id[i], percent[i]])

sorted_list_percent = sorted(merged_list_percent)


# # print header for csv
# for i in range(len(park_name)):
#     print("'" + str(sorted_list[i][1]) + "'", end=',\n')

# clean sorted percent-list
for i in range(len(sorted_list_percent)):
    cleaned_percent.append(sorted_list_percent[i][1])


data = timestamp + cleaned_percent
# print(data)

# write data into csv
with open(path, 'a', encoding='utf8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(data)
    print(TS + ': Data collecting successful!')


print(sorted_list_percent)
