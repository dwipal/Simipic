from external.boxdotnet import BoxDotNet, BoxDotNetError
from lib.genericitems import *

from tornado.options import options

class BoxAuthError(Exception):
    pass

class BoxDriver(object):
    
    def __init__(self, authdata=None):
        self.api_key = options.box_api_key
        
        if authdata:
            self.authdata = authdata
            print "Boxdriver authdata %s"%authdata
        else:
            self.authdata = {}
    
    def get_content(self, root_id):
        
        box = self._get_box_obj_with_ticket()
        boxtree = None
        
        token = self.authdata.get('token', None)
        
        if not token:
            raise BoxAuthError("No Token")
        
        try:
            boxtree = box.get_account_tree(api_key=self.api_key,
                            auth_token = self.authdata['token'], folder_id=root_id,
                            params=["nozip", "onelevel"])
        except BoxDotNetError, bne:
            if bne.status == "not_logged_in":
                raise BoxAuthError()
        
        m = {} 
        if boxtree:
            m['rootfolder'] = self.__get_root_folder(boxtree)
            m['folders'] = self.__get_folders(boxtree)   
            m['files'] = self.__get_files(boxtree)
        else:
            m['rootfolder'] = None
            m['folders'] = None
            m['files'] = None
        return m

    
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
                if f['file_name'].lower().endswith("jpg"):
                    bf = BoxFile()
                    bf.parent_id = rootfolder['id']
                    bf.name = f['file_name']
                    bf.id = f['id']
                    bf.size = f['size']

                    bf.large_thumbnail = f['large_thumbnail']
                    bf.preview_thumbnail = f['preview_thumbnail']
                    files.append(bf)
                
        return files
    
    
    def __get_folders(self, boxtree):
        folders = []        

        boxtree = boxtree.tree[0]
        rootfolder = boxtree.folder[0]
        
        if 'folders' in rootfolder.__dict__:
            for f in rootfolder.folders[0].folder:                
                bf = BoxFolder()
                bf.parent_id = rootfolder['id']
                bf.name = f['name']
                bf.id = f['id']
                bf.size = f['size']

                bf.filecount = f['file_count']
                
                folders.append(bf)
        
        return folders

    def init_auth(self):
        self._get_box_obj_with_ticket()
        
    def init_auth_token(self):
        box = self._get_box_obj_with_ticket()
        rsp = box.get_auth_token(api_key=self.api_key, ticket=self.authdata['ticket'])
        token = rsp.auth_token[0].elementText
        
        self.authdata['token'] = token

    def _get_box_obj_with_ticket(self):
        box = BoxDotNet()
        
        ticket = self.authdata.get('ticket', None)
            
        #print "ticket: %s"%ticket        
        if not ticket:
            rsp = box.get_ticket (api_key=self.api_key)
            ticket = rsp.ticket[0].elementText        
            self.authdata['ticket'] = ticket
            print "Generated new ticket %s"%ticket
            
        self.auth_url = "http://www.box.net/api/1.0/auth/%s" % ticket
        return box
        
