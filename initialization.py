import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from pandas.io.json import json_normalize
import os
import time
import re
import html

# You have to follow instructions here : http://dcs.gla.ac.uk/~richardm/TREC_IS/2020/data.html (if no changes)
# and download 'trecis2018-test', 'trecis2018-train', 'trecis2019-A-test' and 'trecis2019-B-test' sets'

# Map TREC IS annotators event labels to event label
d_map = {'costaRicaEarthquake2012':'costaRicaEarthquake2012',
		'fireColorado2012':'fireColorado2012',
		'floodColorado2013':'floodColorado2013',
		'typhoonPablo2012':'typhoonPablo2012',
		'laAirportShooting2013':'laAirportShooting2013',
		'westTexasExplosion2013':'westTexasExplosion2013',
		'guatemalaEarthquake2012':'guatemalaEarthquake2012',
		'bostonBombings2013':'bostonBombings2013',
		'flSchoolShooting2018':'flSchoolShooting2018',
		'chileEarthquake2014':'chileEarthquake2014',
		'joplinTornado2011':'joplinTornado2011',
		'typhoonYolanda2013':'typhoonYolanda2013',
		'queenslandFloods2013':'queenslandFloods2013',
		'nepalEarthquake2015S3':'nepalEarthquake2015',
		'nepalEarthquake2015':'nepalEarthquake2015',
		'australiaBushfire2013':'australiaBushfire2013',
		'philipinnesFloods2012':'philipinnesFloods2012',
		'albertaFloods2013':'albertaFloods2013',
		'nepalEarthquake2015S2':'nepalEarthquake2015',
		'typhoonHagupit2014S2':'typhoonHagupit2014',
		'manilaFloods2013':'manilaFloods2013',
		'parisAttacks2015':'parisAttacks2015',
		'italyEarthquakes2012':'italyEarthquakes2012',
		'typhoonHagupit2014':'typhoonHagupit2014',
		'typhoonHagupit2014S1':'typhoonHagupit2014',
		'nepalEarthquake2015S4':'nepalEarthquake2015',
		'nepalEarthquake2015S1':'nepalEarthquake2015',
		'floodChoco2019':'floodChoco2019',
		'earthquakeCalifornia2014':'earthquakeCalifornia2014',
		'shootingDallas2017A':'shootingDallas2017',
		'earthquakeBohol2013':'earthquakeBohol2013',
		'fireYMM2016E':'fireYMM2016',
		'shootingDallas2017E':'shootingDallas2017',
		'hurricaneFlorence2018A':'hurricaneFlorence2018',
		'hurricaneFlorence2018B':'hurricaneFlorence2018',
		'fireYMM2016A':'fireYMM2016',
		'hurricaneFlorence2018C':'hurricaneFlorence2018',
		'hurricaneFlorence2018D':'hurricaneFlorence2018',
		'fireYMM2016B':'fireYMM2016',
		'shootingDallas2017B':'shootingDallas2017',
		'shootingDallas2017C':'shootingDallas2017',
		'fireYMM2016D':'fireYMM2016',
		'philippinesEarthquake2019A':'philippinesEarthquake2019',
		'philippinesEarthquake2019C':'philippinesEarthquake2019',
		'philippinesEarthquake2019B':'philippinesEarthquake2019',
		'southAfricaFloods2019C':'southAfricaFloods2019',
		'cycloneKenneth2019B':'cycloneKenneth2019',
		'albertaWildfires2019A':'albertaWildfires2019',
		'albertaWildfires2019B':'albertaWildfires2019',
		'coloradoStemShooting2019A':'coloradoStemShooting2019',
		'coloradoStemShooting2019C':'coloradoStemShooting2019',
		'coloradoStemShooting2019B':'coloradoStemShooting2019',
		'cycloneKenneth2019A':'cycloneKenneth2019',
		'southAfricaFloods2019A':'southAfricaFloods2019',
		'cycloneKenneth2019C':'cycloneKenneth2019',
		'southAfricaFloods2019B':'southAfricaFloods2019',
		'philippinesEarthquake2019D':'philippinesEarthquake2019',
		'sandiegoSynagogueShooting2019A':'sandiegoSynagogueShooting2019',
		'sandiegoSynagogueShooting2019C':'sandiegoSynagogueShooting2019',
		'sandiegoSynagogueShooting2019B':'sandiegoSynagogueShooting2019',
		'albertaWildfires2019C':'albertaWildfires2019',
		'albertaWildfires2019D':'albertaWildfires2019',
		'cycloneKenneth2019D':'cycloneKenneth2019',
# Labels below are not taking into account in our paper, we did not have them at the time we wrote it 
		'fireYMM2016C':'fireYMM2016',
		'shootingDallas2017D':'shootingDallas2017'}

tweet_id_map = {}

PATH_json = "./TREC IS annotations/TRECIS_2018_2019-labels.json"
PATH_tweets = "./Tweets/"

"""
---------------------------------------------------------------------------------------------
Association tweets-annotations
---------------------------------------------------------------------------------------------
"""

with open(PATH_json, "r",encoding='ISO-8859-1') as file:
	tweets = json.load(file)
	for tweet in tweets:
		if tweet["eventID"] != 'fireYMM2016C' and tweet["eventID"] != 'shootingDallas2017D':
			tweet_id_map[tweet["postID"]]={}
			tweet_id_map[tweet["postID"]]["categories"]=tweet["postCategories"]
			tweet_id_map[tweet["postID"]]["priority"]=tweet["postPriority"]
			tweet_id_map[tweet["postID"]]["event"]=d_map[tweet["eventID"]]

l_encoding = ["albertaWildfires2019","coloradoStemShooting2019","cycloneKenneth2019","earthquakeBohol2013","fireYMM2016",
"joplinTornado2011","manilaFloods2013","philippinesEarthquake2019","sandiegoSynagogueShooting2019",
"shootingDallas2017","southAfricaFloods2019"]

for files in tqdm(os.listdir(PATH_tweets)):
	if not files.startswith('.'):
		with open(PATH_tweets+files, "r",encoding='UTF-8') as file:
			for line in file:
				tweet = json.loads(line)
				if tweet["allProperties"]["id"] in tweet_id_map:
					tweet_id_map[tweet["allProperties"]["id"]]["text"] = tweet["allProperties"]["text"]
					src = json.loads(tweet["allProperties"]["srcjson"])
					if "created_at" in src:
						if "+0000" in src["created_at"]:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
						else:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["created_at"],'%b %d, %Y %H:%M:%S %p'))
					else:
						if "+0000" in src["createdAt"]:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["createdAt"],'%a %b %d %H:%M:%S +0000 %Y'))
						else:
							tweet_id_map[tweet["allProperties"]["id"]]["timestamp"] = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(src["createdAt"],'%b %d, %Y %H:%M:%S %p'))
					if "user.id_str" in tweet["allProperties"]:
						tweet_id_map[tweet["allProperties"]["id"]]["user_id_str"] = tweet["allProperties"]["user.id_str"]
					else:
						tweet_id_map[tweet["allProperties"]["id"]]["user_id_str"] = tweet["allProperties"]["user.id"]

tweet_id_json = []
for i in tweet_id_map:
	tweet_id_json.append(dict(id=i,content=dict(tweet_id_map[i])))

df = pd.DataFrame.from_dict(json_normalize(tweet_id_json), orient='columns')

# The tweets ids were reported High Priority or News by one of the TREC assessor in the first version of the data gave by TREC
l_ids_other_assessor = ['1040371051706953728','1041619713078571008','1040360701586489344',
'1040599786125185024','1040614324681826305','1040205012117479424','1040622759368421376','1041401444669288448','1039920284827086848']

def high_priority(priority,ids):
	if priority in ["High","Critical"] or ids in l_ids_other_assessor:
		return True
	return False

def news(categories,ids):
	for i in categories:
		if i=="ContinuingNews" or i=="News":
			return True
	if ids in l_ids_other_assessor:
		return True
	return False


def cleanRaw(x):
	x=' '.join(x.split())
	x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
	x=html.unescape(x)
	x=' '.join(x.split())
	return x

def clean(x):
	x=' '.join(x.split())
	x=re.sub(r'&amp;','&',x,flags=re.MULTILINE)
	x=html.unescape(x)
	x=re.sub(r'http\S+','',x, flags=re.MULTILINE)
	# to remove links that start with HTTP/HTTPS in the tweet
	x=re.sub(r'[-a-zA-Z0–9@:%._\+~#=]{0,256}\.[a-z]{2,6}\b([-a-zA-Z0–9@:%_\+.~#?&//=]*)','',x, flags=re.MULTILINE) 
	# to remove other url links
	x=re.sub(r"@(\w+)", '',x, flags=re.MULTILINE)
	x=' '.join(x.split())
	return x

def _surrogatepair(match):
	char = match.group()
	assert ord(char) > 0xffff
	encoded = char.encode('UTF-8')
	return (
		chr(int.from_bytes(encoded[:2], 'little')) + 
		chr(int.from_bytes(encoded[2:], 'little')))

def with_surrogates(text):
	return _nonbmp.sub(_surrogatepair, text)

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')
# _nonbmp = re.compile(r'[\U0800-\UFFFF]'))


# Order tweets with twin timestamps
l_twin_timestamp_order = [["665284743156637696","665284742686773248"],
["727629011728224256","727629009207463937"],
["727630033846603776","727630033288712192"],
["1121111562779938816","1121111562704437248"],
["1121111567594950656","1121111566324101120"],
["1121111566324101120","1111567943327744"],
["1122228237365587970","1122228235658518531"],
["1125882096403320833","1125882096877281280"]]


def timestamp_ordering(df,list_timestamp):
	l_df_order = []
	for i in df["id"]:
		if i in list_timestamp:
			l_df_order.append(i)
	if list_timestamp[0]!=l_df_order[0]:
		l1 = list(df.index[df["id"]==list_timestamp[0]])[0]
		l2 = list(df.index[df["id"]==list_timestamp[1]])[0]
		temp = df.loc[l1].copy()
		df.loc[l1] = df.loc[l2]
		df.loc[l2] = temp
	return df

"""
Create events file with all tweets
"""

for i in df["content.event"].unique():
	if os.path.exists('./Données/Tweets/'+i+'.txt'):
		os.remove('./Données/Tweets/'+i+'.txt')
	for j in df[df["content.event"]==i]["content.text"]:
		with open('./Données/Tweets/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(cleanRaw(j))+'\n')


df_summary = df[df.apply(lambda x: high_priority(x["content.priority"],x["id"]),axis=1)]
df_summary = df_summary[df_summary.apply(lambda x: news(x["content.categories"],x["id"]),axis=1)]
df_summary["content.timestamp"] = pd.to_datetime(df_summary["content.timestamp"])
df_summary = df_summary.sort_values(by=["content.timestamp"])
for i in l_twin_timestamp_order:
	df_summary = timestamp_ordering(df_summary,i)

"""
Create NHP events file with News High Priority tweets
"""

for i in df_summary["content.event"].unique():
	if os.path.exists('./Données/Résumés/'+i+'.txt'):
		os.remove('./Données/Résumés/'+i+'.txt')
	for j in df_summary[df_summary["content.event"]==i]["content.text"]:
		with open('./Données/Résumés/'+i+'.txt','a',encoding='UTF-8') as file:
			file.write(with_surrogates(clean(j))+'\n')