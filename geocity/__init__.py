import sys
import os
import csv
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

        
def _get_city_db():
    csv.field_size_limit(sys.maxsize)
    cities_file = os.path.join(os.path.dirname(__file__), 'cities.txt')
    with open(cities_file, 'rb') as f:
        r = csv.reader(f, delimiter='\t')
        city_db = list(r)
        return city_db

    
class City(object):
    """
    City GEO info class
    >>> City(city='petah tiqwa', cc='IL')
    >>> c.latitude
    32.08707
    """
    CITY_DB = _get_city_db()

    def __init__(self, city="jerusalem", cc="IL"):
        """
        get city name and optional country code
        """
        self._city = city
        self._country_code = cc
        self._info = self.find_city(city, cc)

    def get_info(self):
        return self._info

    def __repr__(self):
        return "City '{name}': lat:{latitude}, long:{longitude}, cc:{country_code} elevation:{elevation}, timezone:{timezone}\nAlternative names: {alternatenames}".format(**self._info)

    def find_cities(self, city, country=None):
        res = []
        for i in self.CITY_DB:
            if not country or country in i[8]:
                if (city.lower() in i[3].lower()):
                    res.append(dict(name=i[1], asciiname=i[2], alternatenames=i[3], latitude=float(i[4]), longitude=float(i[5]), country_code=i[8], elevation=int(i[16]), timezone=i[17]))
        return res

    def find_city(self, city, country=None):
        res = self.find_cities(city, country=None)
        if not len(res):
            raise IndexError('No match')
        elif len(res) > 1:
            raise IndexError('Too many matches ({})'.format(len(res)))
        return res[0]

    @property
    def latitude(self):
        return self.get_info()['latitude']

    @property
    def longitude(self):
        return self.get_info()['longitude']

    @property
    def elevation(self):
        return self.get_info()['elevation']

    @property
    def timezone(self):
        return self.get_info()['timezone']

    @property
    def names(self):
        return self.get_info()['alternatenames']
