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
        box = self._get_box_obj_with_ticket()
        url = "http://www.box.net/api/1.0/auth/%s" % box.ticket
        self.redirect(url)
    
class AuthBoxDoneHandler(AlbumsHandler):
    @tornado.web.authenticated
    def get(self):
        box = self._get_box_obj_with_ticket()
        rsp = box.get_auth_token(api_key=box.api_key, ticket=box.ticket)
        token = rsp.auth_token[0].elementText
        
        
        authdata = {'ticket': box.ticket, 'token': token}        
        self.cdata.add_auth(self.get_current_user()['email'], "box", authdata)
        
        self.redirect("/albums")
        
