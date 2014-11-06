#!/usr/bin/python

import json
import urllib2
import json
import csv
import MySQLdb

target_url = "http://api.eia.gov/category/?api_key=45780D1A92A4F363815C75600ACF5748&category_id=479754"
server_url = "eia.cwvrtrnm3ga3.us-west-2.rds.amazonaws.com"
api_data = json.load(urllib2.urlopen(target_url))
file = open('state.csv', 'rb')


db = MySQLdb.connect(server_url,"observ","forecast123","eiadev" )
print "connecting to the database..."
cursor = db.cursor()
insert_command = ("INSERT INTO state"
              "(id, name, region_id, eia_category_id) "
              "VALUES (%s, %s, %s, %s)")

# insert data from state csv
for row in csv.DictReader(file):
	id = row['state_id']
	name = row['name']
	insert_data = (id, name, None, None)
	print "inserting...", id, name
	cursor.execute(insert_command,insert_data)
db.commit()

# insert eia_category_id from eia site
update_command = ("UPDATE state SET eia_category_id = %s WHERE name = %s ")
value = api_data["category"]["childcategories"]
for data in value:
	print data
	name = data["name"]
	eia_category_id = data["category_id"]
	update_data = (eia_category_id, name)
	cursor.execute(update_command,update_data)
db.commit()


cursor.close()
db.close()