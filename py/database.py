import pymysql
from py.auth import post_init, get_creds
# on import la fx qui permet la recuperation des coords gps sur base du numero de telephonme
from py.gpsdata import get_gpsdata

db = pymysql.connect(host="your-host", port=3310, user="your-user", password="your-password", database="your-databae")
# you have cursor instance here
cursor = db.cursor()

# def pour se connecter en tant que user authentifier
def get_user(username, password):
    #on select tous les populations
    sql = f'''select * from population where username='{username}' and password='{password}';'''
    cursor.execute(sql)
    data = cursor.fetchone()
    if data is None:
        dic = {
            'id':None,
            'username':None,
            'password':None,
            'phonenumber':None
        }
    else:
        dic = {
            'id':data[0],
            'username':data[2],
            'password':data[3],
            'phonenumber':data[5]
        }
    return dic

# insert some records in the table 
def alert(status):
    result = False
    if post_init():
        gps = get_gpsdata()
        data = get_creds()
        user = get_user(data.get('username'), data.get('password'))
        sql = f'''insert into alarm (message, fk_population, log, lat, status) VALUES ('Alerte', '{user.get('id')}', '{gps.get('lng')}', '{gps.get('lat')}', '{status}');'''
        cursor.execute(sql)
        db.commit()
        result = True
    else:
        result = False
    return result

