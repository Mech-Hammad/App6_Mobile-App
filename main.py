# When using kivy, we have to name our script main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
from glob import glob
import json
import random
Builder.load_file('design.kv')  # load the kv design file


class RootWidget(ScreenManager):
    pass


class LoginScreen(Screen):  # Class corresponding to the LoginScreen tag inside our design file
    def my_sign_up(self):
        # make sure it transitions as to move forward here
        self.manager.transition.direction = "left"
        self.manager.current = "signup_screen"

    def check_login(self, inp_name, inp_password):
        with open('users.json', 'r') as file:
            users = json.load(file)

        user = users.get(inp_name)
        if user is not None:  # user by that username exists
            if user["password"] == inp_password:
                self.login_success()

        self.login_failure()

    def login_success(self):
        # make sure it transitions as to move forward here
        self.manager.transition.direction = "left"
        self.manager.current = "home_screen"

    def login_failure(self):
        self.ids.wrong_credentials.text = "Wrong Username or Password!"


class SignupScreen(Screen):
    def add_user(self, name, password):  # kivy app passes the arguments to this function
        with open('users.json') as file:
            users = json.load(file)

        users[name] = {
            'username': name,
            'password': password,
            'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        }
        print(users)
        with open('users.json', 'w') as file:
            json.dump(users, file)

        self.manager.current = "sign_up_success_screen"


class SignUpSuccessScreen(Screen):
    def redirect_to_login(self):
        # so it appears to go back to loginscreen
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.quotes = self.read_quotes_from_file()  # init as empty dict

    def read_quotes_from_file(self):
        # return a dict containing lists of quotes for moods
        quotes = {}
        for name in glob('quotes/*.txt'):
            with open(name, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # get filename from file path and then get name without extension
                mood_name = name.split('\\')[-1].split('.')[0]
                quotes[mood_name] = lines
        return quotes

    def logout(self):
        # so it appears to go back to loginscreen
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def change_mood(self, user_mood):
        user_mood_text = user_mood.lower()
        self.make_happy(user_mood_text)

    def make_happy(self, user_mood_text):
        ls = self.quotes.get(user_mood_text)
        if ls is not None:  # key exists in dictionary
            self.ids.mood_text.text = random.choice(ls)
        else:  # don't have quotes for the inputted mood
            self.ids.mood_text.text = "You are impossible!"


class ImageButton(ButtonBehavior, Image, HoverBehavior):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()  # returns RootWidget object


if __name__ == "__main__":
    MainApp().run()  # run method on instance of MainApp
