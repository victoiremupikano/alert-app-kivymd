import pathlib 
import json
import os

# this file path is insecure
cred_path: pathlib.Path = pathlib.Path("creds.json")

def post_init():
    # resultat
    result = False
    if cred_path.exists(): 
        result = True
    else:
        result = False
    return result
            
# def pour retourner les creds
def get_creds():
    try:
        data = json.loads(cred_path.read_text())
    except Exception:
        print("Erreur de reuperation des données")
        data = None
    if data is None:
        clear_creds()
    else:
        username = data.get('username')
        password = data.get('password')
        phonenumber = data.get('phonenumber')
        dic = {
            'username':username,
            'password':password,
            'phonenumber':phonenumber
        }
    return dic

def write_creds(data:dict):
    """
    Store credentials as a local file
    and update instance with correct
    data.
    """
    if cred_path is not None:
        username = data.get('username')
        password = data.get('password')
        if username and password:
            cred_path.write_text(json.dumps(data))

def clear_creds():
    result = False
    if cred_path.exists():
        os.remove(cred_path)
        if not os.path.exists(cred_path):
            result = True
        else:
            result = False
    return result