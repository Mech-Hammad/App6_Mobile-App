# When using kivy, we have to name our script main.py

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
import json
from datetime import datetime
Builder.load_file('design.kv')  # load the kv design file


class RootWidget(ScreenManager):
    pass


class LoginScreen(Screen):  # Class corresponding to the LoginScreen tag inside our design file
    def my_sign_up(self):
        self.manager.transition.direction = "left" # make sure it transitions as to move forward here
        self.manager.current = "signup_screen"

    def check_login(self, inp_name, inp_password):
        with open('users.json', 'r') as file:
            users = json.load(file)

        user =  users.get(inp_name)
        if user is not None: # user by that username exists
            if user["password"] == inp_password:
                self.login_success()
        
        self.login_failure()
                
    def login_success(self):
        self.manager.transition.direction = "left" # make sure it transitions as to move forward here
        self.manager.current = "signup_screen"

    def login_success(self):
        pass


class SignupScreen(Screen):
    def add_user(self, name, password): # kivy app passes the arguments to this function
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
        self.manager.transition.direction = "right" # so it appears to go back to loginscreen
        self.manager.current = "login_screen"
        

class HomeScreen(Screen):
    def logout(self):
        self.manager.transition.direction = "right" # so it appears to go back to loginscreen
        self.manager.current = "login_screen"


class MainApp(App):
    def build(self):
        return RootWidget()  # returns RootWidget object


if __name__ == "__main__":
    MainApp().run()  # run method on instance of MainApp
