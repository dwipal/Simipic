import tornado.web
import tornado.escape

from base import BaseHandler
from lib.genericitems import *
from lib.boxdriver import *

from external.boxdotnet import BoxDotNet

class AlbumsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        boxauth = self.cdata.get_auth(self.get_current_user()['email'], "box")
        
        if boxauth:        
            return self._get_albums(boxauth)
        else:
            self.redirect("/auth/box")
        
        
    def _get_albums(self, boxauth):
        root_id = self.get_argument("root_id", "0")
        
        bd = BoxDriver(boxauth)
        m = bd.get_content(root_id)
        m['title'] = m['rootfolder']['name']
        
        return self.render_template("albums", m)
        
        
class AuthBoxHandler(AlbumsHandler):
    @tornado.web.authenticated
    def get(self):
        bd = BoxDriver()
        bd.init_auth()
        
        self.cdata.add_auth(self.get_current_user()['email'], "box", bd.authdata)
        
        self.redirect(bd.auth_url)
    
class AuthBoxDoneHandler(AlbumsHandler):
    @tornado.web.authenticated
    def get(self):
        authdata = self.cdata.get_auth(self.get_current_user()['email'], "box")
        
        authdata['ticket'] = self.get_argument("ticket", None)
        authdata['token'] = self.get_argument("auth_token", None)

        print "Adding auth %s"%authdata
        self.cdata.add_auth(self.get_current_user()['email'], "box", authdata)
        
        bd = BoxDriver(authdata)
        bd.init_auth_token()
        
        self.redirect("/albums")
        
