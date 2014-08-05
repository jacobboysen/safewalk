import csv
import pymysql as mdb
import pandas as pd
import numpy as np
import matplotlib as plt
from pandas.io import sql
from np import random.normal

#
#keep 0/DATE                              object
#keep 1/TIME                              object
#keep 2/BOROUGH                           object
#3keep ZIP CODE                         float64
#4toss	LATITUDE                         float64
#5toss	LONGITUDE                        float64
#6keep LOCATION                          object
#7keep ON STREET NAME                    object
#8keep CROSS STREET NAME                 object
#9toss OFF STREET NAME                   object
#10keep NUMBER OF PERSONS INJURED          int64
#11	NUMBER OF PERSONS KILLED           int64
#12	NUMBER OF PEDESTRIANS INJURED      int64
#13	NUMBER OF PEDESTRIANS KILLED       int64
#14	NUMBER OF CYCLIST INJURED          int64
#15	NUMBER OF CYCLIST KILLED           int64
#16	NUMBER OF MOTORIST INJURED         int64
#17	NUMBER OF MOTORIST KILLED          int64
#18toss	CONTRIBUTING FACTOR VEHICLE 1     object
#19toss	CONTRIBUTING FACTOR VEHICLE 2     object
#20toss	CONTRIBUTING FACTOR VEHICLE 3     object
#21toss	CONTRIBUTING FACTOR VEHICLE 4     object
#22toss	CONTRIBUTING FACTOR VEHICLE 5     object
#23keep	UNIQUE KEY                         int64



#load crash data, insert into sql db
data_path = r'/Users/boysej01/safewalk/data/NYPD_Motor_Vehicle_Collisions.csv'
#pandas df code if needed
#first read it in and get a list of col header namespace
df = pd.read_csv(data_path)
hd_list = list(df.columns.values)
#delete col(4,5,9,18,19,20,21,22)
#4,5 = lat/long, already in location col #6
#9 'off street name' messy, often NaN
#18-22 contributing factor vehicle cols, info not of immed value

new_df = df[['DATE', 'TIME', 'BOROUGH', 
 'ZIP CODE', 'LATITUDE', 'LONGITUDE', 'LOCATION',
 'ON STREET NAME', 'CROSS STREET NAME', 
 'NUMBER OF PERSONS INJURED', 'NUMBER OF PERSONS KILLED', 
 'NUMBER OF PEDESTRIANS INJURED', 'NUMBER OF PEDESTRIANS KILLED', 
 'NUMBER OF CYCLIST INJURED', 'NUMBER OF CYCLIST KILLED',
 'NUMBER OF MOTORIST INJURED','NUMBER OF MOTORIST KILLED', 
 'UNIQUE KEY']]

#set sql params
#step one: create db in mysql
#mysql -u root -p
#enter pass MEKaokmK
#>create database accident_table;
#step two; run pycode
#step three: show databases/tables to verify
#for raw mysql code:
#LOAD DATA INFILE '/Users/boysej01/safewalk/data/NYP_Motor_Vehicle_Collisions.csv' INTO TABLE accident_table FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;

con = mdb.connect(user="root", host="localhost", db="safewalk_db", passwd="MEKaokmK") 
#pandas workaround to clean up 'nan' with 'None' to avoid pandas sql error throw
new_df = new_df.where(pd.notnull(df), None)
#pass in sql table via pandas; can modify if_exists to 'append' if necessary
new_df.to_sql(con=con, name='accident_table', if_exists='replace', flavor='mysql')

#sum ped injuries and ped killed for each intersection
#populate dicts
inj_dict = {}
mort_dict = {}

with con:
	cur = con.cursor(mdb.cursors.DictCursor)
	cur.execute("SELECT location, sum(NUMBER_OF_PEDESTRIANS_INJURED), sum(NUMBER_OF_PEDESTRIANS_KILLED) FROM accident_table GROUP BY location")
	rows = cur.fetchall()
	for row in rows:
		loc = row["location"]
		if loc is None:
			continue
		else:
			ped_inj = row["sum(NUMBER_OF_PEDESTRIANS_INJURED)"]
			ped_mort = row["sum(NUMBER_OF_PEDESTRIANS_KILLED)"]
			

		


			inj_dict[loc] = ped_inj
			mort_dict[loc] = ped_mort

#rough math alert!
#establishing a PSS = pedestrian safety score for each intersection
#death = 1
#injury severity is unk, so will randomly sample from normal distribution
#with subjectively chosen mean of 0.4
#assumes that average REPORTED TO NYPD motor vehicle-ped accidents are "40% of death
#function therefore is C(x,y) = alphaX + betaY
#x = mort, y = injur
#alpha = death coeff, 1
#beta = injury coeff, randomNorm
def pss (x,y):
	pss = 0
	alpha = 1
	if x != 0:
		mu, sigma = 0.4, 0.1
		beta = np.random.normal(mu, sigma,y)





#mort_only_dict = {}
#ped_only_dict = {}
#both_dict = {}
#no_coll_dict = {}

#if ped_inj > 0:
#	if ped_mort == 0:
#		inj_only_dict[loc] == 1
#	if ped_mort > 0:
#		both_dict[loc] == 1
		
#elif ped_inj == 0:
#	if ped_mort == 0:
#		no_coll_dict[loc] == 1
#	if ped_mort > 0:
#		mort_only_dict[loc] = 1


#BEWARE THE NULL LOCATION 'OUTLIER'? not finding any null value, mysql may be skipping

#stats on locations
#median/std dev for inj/mort



#get mort, inj
#if mort = 0, and inj > 0, record loc and set inj_no_mort to 1
#if opp, set mort_no_inj to 1
#if neither, set no_ped_collisions_dict{loc} to 1




#USE accident_table;
#SELECT location, sum(NUMBER OF PEDESTRIANS XXXX) FROM accident_table group by 

#SELECT location, sum(number_of_pedestrians_injured) FROM accident_table GROUP BY location LIMIT 5;
#SELECT sum(number_of_pedestrians_injured) FROM accident_table;
#2292 ped injuries map to NULL location, 23999 injuries in total (9.6%)
#SELECT location, sum(number_of_pedestrians_injured) FROM accident_table GROUP BY location ORDER BY sum(number_of_pedestrians_injured) DESC LIMIT 5;
#| location                  | sum(number_of_pedestrians_injured) |
#+---------------------------+------------------------------------+
#| NULL                      |                               2292 |
#| (40.6687978, -73.9311201) | Utica and Eastern Pkwy                                31 |
#| (40.8133899, -73.9562587) | 125th and Amsterdam                                28 |
#| (40.7572323, -73.9897922) | 8th AVE and 42nd                            26 |
#| (40.7589746, -73.9189996) | Broadway and Steinway                                24 |
#+---------------------------+------------------------------------+

#data is in sqldb, can be manipulated via pysql
#TO DO

#stats
#distribution of each intersection


#for each location:
#-get number of ped killed, inj
#-calculate ped safety score based on weighting 70/30
#-generate Z-scores for killed, inj, ped safety score

#user interface
#use goolge maps api
#user enters start, target
#google calculates routes
#get routes from array
#get all intersections from array, sum safety scores
#







#vanilla python read
#f = open(data_path, 'rb')
#reader = csv.reader(f)
#rownum = 0
#loc_dict ={}

#for each row
#grab location, or dispose if no location


#compute ped_safety_score
#z-score for each 


for row in reader:
	print "open"
	if rownum == 0:
		header = row
	else:
		colnum = 0
		for col in row:


#group by location to generate weighted nodes
#key = location, value = crash stats #

#pull in nyc location? use goolge maps?