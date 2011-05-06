import tornado.web
import tornado.auth

from model.coredata import CoreData

from base import BaseHandler


class AuthLandingHandler(BaseHandler):
    def get(self):
        return self.render_template("auth_landing")
class AuthHandler(BaseHandler):
    def get(self):
        self.write('<html><body><form action="/auth/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>')
    
               
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")
        
class GoogleAuthHandler(BaseHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authenticate_redirect()
    
    
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
            
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("Logged out.")

        #self.redirect("/")


