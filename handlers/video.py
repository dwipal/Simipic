import tornado.web
import tornado.escape

from base import BaseHandler

class VideoHandler(BaseHandler):
    
    def get(self):
       url = self.get_argument("url")
       m={}
       m['title'] = "Video Player"
       m['video_url'] = url
       return self.render_template("video", m)

