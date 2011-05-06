import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import os

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("host", default='', help="host/ip to bind", type=str)
#from handlers import handlers_list

class Application(tornado.web.Application):
    def __init__(self):
        exec "from handlers import handlers_list"
        handlers = handlers_list
        
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="32oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            login_url="/auth/landing",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()


    

