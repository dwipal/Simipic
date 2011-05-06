from handlers.home import HomeHandler
from handlers.auth import AuthHandler
from handlers.auth import LogoutHandler
from handlers.albums import *

handlers_list = [
	(r"/", HomeHandler),
	(r"/auth/login", AuthHandler),
	(r"/auth/logout", LogoutHandler),
	(r"/albums", AlbumsHandler),
	(r"/auth/box", AuthBoxHandler),
	(r"/auth/box_done", AuthBoxDoneHandler),
]


