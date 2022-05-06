from django.db import models
import requests

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        

# need to write a function to fetch all the countries and cities from an API and populate the database
def populate_countires_and_cities():
    url = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/countries%2Bcities.json'
    data = requests.get(url).json()
    for country in data:
        country_obj = Country.objects.get_or_create(name=country['name'])
        for city in country['cities']:
            city_obj = City.objects.get_or_create(country=country_obj[0], name=city['name'])
                