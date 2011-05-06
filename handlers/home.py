import tornado.web
import tornado.escape

from base import BaseHandler

class HomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.render_template("home")
        
    