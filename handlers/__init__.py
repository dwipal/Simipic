from handlers.home import *
from handlers.auth import *
from handlers.register import *
from handlers.albums import *

from model.coredata import CoreData

cdata = CoreData()

handlers_list = [
	(r"/", HomeHandler, dict(cdata=cdata)),
	(r"/auth/register", RegisterHandler, dict(cdata=cdata)),
	
	(r"/auth/landing", AuthLandingHandler, dict(cdata=cdata)),
	(r"/auth/login", AuthHandler, dict(cdata=cdata)),
	(r"/auth/login_google", GoogleAuthHandler, dict(cdata=cdata)),
	
	
	(r"/auth/logout", LogoutHandler, dict(cdata=cdata)),
	(r"/albums", AlbumsHandler, dict(cdata=cdata)),
	(r"/auth/box", AuthBoxHandler, dict(cdata=cdata)),
	(r"/auth/box_done", AuthBoxDoneHandler, dict(cdata=cdata)),
]

