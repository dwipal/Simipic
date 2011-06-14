import tornado.web
import tornado.escape

from base import BaseHandler
from lib.genericitems import *
from lib.boxdriver import *

from external.boxdotnet import BoxDotNet

class AlbumsHandler(BaseHandler):
    def get(self):
        cuser = self.get_current_user()
        
        username = self.get_argument("username", None)
        if username:            
            if not self.get_current_user() or self.get_current_user()['email'] != username:
                cuser = self.cdata.get_user(username)
            
        if not cuser:
            self.redirect("/")
        boxauth = self.cdata.get_auth(cuser['email'], "box")
        
        if boxauth:
            try:
                return self._get_albums(cuser, boxauth)
            except BoxAuthError, bae:
                self.redirect("/auth/box")
        else:
            self.redirect("/auth/box")
        
        
    def _get_albums(self, cuser, boxauth):
        root_id = self.get_argument("root_id", "0")
        
        fetch_updates = self.get_argument("updates", None) == "1"
        print "fetch_updates: %s"%fetch_updates
        
        bd = BoxDriver(boxauth)
        m = bd.get_content(root_id, fetch_updates = fetch_updates)
        if m['rootfolder']:
            m['title'] = m['rootfolder']['name']
            m['share_link'] = m['rootfolder']['shared_link']        
        else:
            m['title'] = "Nothing to see here. Move along.."
        m['cuser'] = cuser
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
        
