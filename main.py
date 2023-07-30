from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
# on importe les fx de l'auth
from py.auth import post_init, get_creds, write_creds, clear_creds
# on import pour l'acces a la db
from py.database import get_user, alert
# message box
from kivymd.uix.snackbar import Snackbar
from kivy.metrics import dp

#Taille de la fenetre
Window.size = (450, 780)

class UORAlert(MDApp):
    def login(self, username, password):
        if post_init():
            data = get_creds()
            if data.get('username') != "" or data.get('password') != "":
                screen_manager.transition.direction = "left"
                screen_manager.current = "home_genrale"
            else:
                sb = Snackbar(text="Votre compte n'est plus valide !", font_size="12sp", opacity=1)
                sb.ids.text_bar.text_color = "white"
                sb.open()
        else:
            if username == "" or password == "":
                sb = Snackbar(text="Nom d'utisateur ou mot de passe est(sont) vide(s) !", font_size="12sp", opacity=1)
                sb.ids.text_bar.text_color = "white"
                sb.open()
            else:
                user = get_user(username, password)
                if user.get('id') is None:
                    sb = Snackbar(text="Erreur, vous n'avez pas de compte authentifier !", font_size="12sp", opacity=1)
                    sb.ids.text_bar.text_color = "white"
                    sb.open()
                else:
                    dict = {"username":user.get('username'), "password":user.get('password'), "phonenumber":user.get('phonenumber')}
                    write_creds(dict)
                    if post_init():
                        data = get_creds()
                        if data.get('username') != "" or data.get('password') != "":
                            screen_manager.transition.direction = "left"
                            screen_manager.current = "home_genrale"
                        else:
                            sb = Snackbar(text="Votre compte n'est pas valide !", font_size="12sp", opacity=1)
                            sb.ids.text_bar.text_color = "white"
                            sb.open()

    def logout(self):
        if clear_creds():
            screen_manager.transition.direction = "right"
            screen_manager.current = "signup"
        else:
            sb = Snackbar(text="Erreur de déconnection !", font_size="12sp", opacity=1)
            sb.ids.text_bar.text_color = "white"
            sb.open()

    def set_alarm(self, status):
        if alert(status):
            sb = Snackbar(text="Alerte envoyer avec succès !", font_size="12sp", opacity=1)
            sb.ids.text_bar.text_color = "white"
            sb.open()
        else:
            sb = Snackbar(text="Alerte non envoyer !", font_size="12sp", opacity=1)
            sb.ids.text_bar.text_color = "white"
            sb.open()

    def unset_alarm(self, status):
        if alert(status):
            sb = Snackbar(text="Alerte démentit avec succès !", font_size="12sp", opacity=1)
            sb.ids.text_bar.text_color = "white"
            sb.open()
        else:
            sb = Snackbar(text="Alerte démentit non envoyer !", font_size="12sp", opacity=1)
            sb.ids.text_bar.text_color = "white"
            sb.open()

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        if post_init():
            data = get_creds()
            if data.get('username') != "" or data.get('password') != "":
                # on charge tous les screens et on affiche le premier
                screen_manager.add_widget(Builder.load_file("kv/home.kv"))
                screen_manager.add_widget(Builder.load_file("kv/signup.kv"))
            else:
                sb = Snackbar(text="Votre compte n'est plus valide !", font_size="12sp", opacity=1)
                sb.ids.text_bar.text_color = "white"
                sb.open()
        else:
            # on charge tous les screens et on affiche le premier
            screen_manager.add_widget(Builder.load_file("kv/signup.kv"))
            screen_manager.add_widget(Builder.load_file("kv/home.kv"))

        return screen_manager

if __name__=="__main__":
    LabelBase.register(name="BMontserrat", fn_regular="assets/Montserrat/static/Montserrat-SemiBold.ttf")
    LabelBase.register(name="MMontserrat", fn_regular="assets/Montserrat/static/Montserrat-Medium.ttf")
        
    UORAlert().run()