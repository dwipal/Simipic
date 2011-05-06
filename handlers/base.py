import tornado.web
import tornado.escape
import os

from Cheetah.Template import Template

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        current_user = self.get_secure_cookie("user")
        if not current_user:
            return None
        
        return current_user
        
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)


    def render_template(self, filename, values_dict=None):
        path = os.path.join(os.path.dirname(__file__), "../templates/%s.tmpl"%filename)

        common_vals = dict(
            user = self.get_current_user(),
            cookies = self.cookies,
            title = "Box",
        )
        
        tmpl = Template( file = path, searchList = (values_dict, common_vals) )
        
        self.write(str(tmpl))
