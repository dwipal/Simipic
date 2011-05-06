import tornado.web
import tornado.auth

from base import BaseHandler


class RegisterHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/auth/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
    
               
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")
        