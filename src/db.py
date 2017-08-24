import psycopg2
import json

""" function to connect to db using credentials specified in config """
def getDBConnection():
    with open('../config/config.json') as json_data:
        data = json.load(json_data)
        data = data['database_credentials']

    try:
        conn = psycopg2.connect(dbname=data['dbname'], user=data['user'], host=data['host'], password=data['password'])
    except:
        print("DB connection failed")
        exit(1)

    return conn
