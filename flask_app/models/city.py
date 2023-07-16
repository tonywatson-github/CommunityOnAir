from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import report, user
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class City:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reports = []
    
    @classmethod
    def cities(cls):
        query = "SELECT * FROM cities;"
        results = connectToMySQL('onair').query_db(query)
        cities = []
        for city in results:
            cities.append(cls(city))
        return cities
    
    @classmethod
    def city_with_reports(cls, id):
        query  = "SELECT * FROM cities LEFT JOIN reports ON reports.city_id = cities.id WHERE cities.id = %(id)s;"
        results = connectToMySQL('onair').query_db(query, id)
        city = cls(results[0])
        for row in results:
            reports_data = {
            'id': row['reports.id'],
            'what': row['what'],
            'location': row['location'],
            'created_at': row['reports.created_at'],
            'updated_at': row['reports.updated_at'],
            'city_id': row['city_id'],
            'user_id': row['user_id']
            }
            city.reports.append(report.Report(reports_data))
        return city
