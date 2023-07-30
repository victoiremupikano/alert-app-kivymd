import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from opencage.geocoder import OpenCageGeocode
from py.auth import post_init, get_creds

def get_gpsdata():
    if post_init():
        data = get_creds()
        num =  data.get('phonenumber')

        # touver le pays du numero
        monNum = phonenumbers.parse(num)
        localisation = geocoder.description_for_number(monNum, "fr")

        # trouver l'operateur du numero
        operateur = phonenumbers.parse(num)

        # trouver la latitude et la longitude
        clef = "61fe5867b0db4fde8f3bed0bc0e35137"
        coord = OpenCageGeocode(clef)
        requette = str(localisation)
        reponse = coord.geocode(requette)
        # extraction de lat et de lng
        lat = reponse[0]["geometry"]["lat"]
        lng = reponse[0]["geometry"]["lng"]

        dic = {
            'lat':lat,
            'lng':lng
            }
    return dic