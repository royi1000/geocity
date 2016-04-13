import sys
import csv
import unicodedata


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

        
def _get_city_db():
    csv.field_size_limit(sys.maxsize)
    with open('cities.txt', 'rb') as f:
        r = csv.reader(f, delimiter='\t')
        city_db = list(r)
        return city_db

    
class City(object):
    """city GEO info class
geonameid         : integer id of record in geonames database
name              : name of geographical point (utf8) varchar(200)
asciiname         : name of geographical point in plain ascii characters, varchar(200)
alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
latitude          : latitude in decimal degrees (wgs84)
longitude         : longitude in decimal degrees (wgs84)
feature class     : see http://www.geonames.org/export/codes.html, char(1)
feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
country code      : ISO-3166 2-letter country code, 2 characters
cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
admin3 code       : code for third level administrative division, varchar(20)
admin4 code       : code for fourth level administrative division, varchar(20)
population        : bigint (8 byte int)
elevation         : in meters, integer
dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
timezone          : the timezone id (see file timeZone.txt) varchar(40)
modification date : date of last modification in yyyy-MM-dd format"""
    CITY_DB = _get_city_db()
    
    def __init__(self, city="jerusalem", cc="IL"):
        """name = tuple(city_name, country_code)"""
        self._city = city
        self._country_code = cc
        self._info = self.find_city(city, cc)

    def set_info(self, city, country):
        for i in self.CITY_DB:
            if country in i[8] and (remove_accents(i[2].decode('utf8')).lower() == remove_accents(city.decode('utf8')).lower()):
                return dict(name=i[1], asciiname=i[2], alternatenames=i[3], latitude=float(i[4]), longitude=float(i[5]), country_code=i[8], elevation=int(i[16]), timezone=i[17])
        raise IndexError

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
