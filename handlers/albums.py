import tornado.web
import tornado.escape

from base import BaseHandler

from external.boxdotnet import BoxDotNet

class AlbumsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.get_secure_cookie('box_token'):
            return self._get_albums()
        else:
            self.redirect("/auth/box")
        
        
    def _get_albums(self):
        root_id = self.get_argument("root_id", "0")
        
        box = self._get_box_obj_with_ticket()
        box_token = self.get_secure_cookie('box_token')
        
        boxtree = box.get_account_tree(api_key=box.api_key,
                            auth_token = box_token, folder_id=root_id,
                            params=["nozip", "onelevel"])
        
        rootfolder = self.__get_root_folder(boxtree)
        m = {}
        m['rootfolder'] = rootfolder
        m['title'] = rootfolder['name']
        m['folders'] = self.__get_folders(boxtree)   
        m['files'] = self.__get_files(boxtree)   
        return self.render_template("albums", m)

    
    def __get_root_folder(self, boxtree):
        boxtree = boxtree.tree[0]
        if boxtree.folder:
            return boxtree.folder[0]
        return None

    def __get_files(self, boxtree): 
        boxtree = boxtree.tree[0]
        rootfolder = boxtree.folder[0]

        files = []
        if 'files' in rootfolder.__dict__:
            for f in rootfolder.files[0].file:
                files.append(f)
                
        return files
    
    def __get_folders(self, boxtree):
        folders = []        

        boxtree = boxtree.tree[0]
        rootfolder = boxtree.folder[0]
        
        if 'folders' in rootfolder.__dict__:
            for f in rootfolder.folders[0].folder:
                folders.append(f)
        
        return folders

    def _get_box_obj_with_ticket(self):
        box = BoxDotNet()
        api_key = "l6ld3bydad6psc505n4p8uz5j3u3ho7h"

        ticket = self.get_secure_cookie("box_ticket")

        #print "ticket: %s"%ticket        
        if not ticket:
            rsp = box.get_ticket (api_key=api_key)
            ticket = rsp.ticket[0].elementText        
            self.set_secure_cookie("box_ticket", ticket)
            
        box.ticket = ticket
        box.api_key = api_key
        
        box.auth_url = "http://www.box.net/api/1.0/auth/%s" % box.ticket
        return box
        
        
        
class AuthBoxHandler(AlbumsHandler):
    def get(self):
        box = self._get_box_obj_with_ticket()
        url = "http://www.box.net/api/1.0/auth/%s" % box.ticket
        self.redirect(url)
    
class AuthBoxDoneHandler(AlbumsHandler):
    def get(self):
        box = self._get_box_obj_with_ticket()
        rsp = box.get_auth_token(api_key=box.api_key, ticket=box.ticket)
                
        self.set_secure_cookie("box_token", rsp.auth_token[0].elementText)
        self.redirect("/albums")
        
