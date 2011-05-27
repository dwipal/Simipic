import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import os

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("host", default='0.0.0.0', help="host/ip to bind", type=str)
define("config", default='development.conf', help="config file name", type=str)
define("box_api_key", default='', help="api key for box.net", type=str)
#from handlers import handlers_list

class Application(tornado.web.Application):
    def __init__(self):
        exec "from handlers import handlers_list"
        handlers = handlers_list
        
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="thebigrandomsecretofhellobox",
            login_url="/auth/landing",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(options.config)
    
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address=options.host)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


    

