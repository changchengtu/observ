import csv
import MySQLdb

server_url = "eia.cwvrtrnm3ga3.us-west-2.rds.amazonaws.com"
file = open('category.csv', 'rb')


db = MySQLdb.connect(server_url,"observ","forecast123","eiadev" )
print "connecting to the database..."
cursor = db.cursor()
insert_command = ("INSERT INTO category"
              "(id, name) "
              "VALUES (%s, %s)")

for row in csv.DictReader(file):
	id = row['category_id']
	name = row['name']
	insert_data = (id, name)
	print "inserting...", id, name
	cursor.execute(insert_command,insert_data)

db.commit()
cursor.close()
db.close()