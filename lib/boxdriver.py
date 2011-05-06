from external.boxdotnet import BoxDotNet
from lib.genericitems import *

class BoxDriver(object):
    
    def __init__(self, boxauth):
        self.api_key = "l6ld3bydad6psc505n4p8uz5j3u3ho7h"
        self.boxauth = boxauth
    
    def get_content(self, root_id):
        
        box = self._get_box_obj_with_ticket()
        
        boxtree = box.get_account_tree(api_key=self.api_key,
                            auth_token = self.boxauth['token'], folder_id=root_id,
                            params=["nozip", "onelevel"])
        
        
        m = {}
        m['rootfolder'] = self.__get_root_folder(boxtree)
        m['folders'] = self.__get_folders(boxtree)   
        m['files'] = self.__get_files(boxtree)   
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

    def _get_box_obj_with_ticket(self):
        box = BoxDotNet()

        ticket = self.boxauth['ticket']
        api_key = self.api_key
        
        #print "ticket: %s"%ticket        
        if not ticket:
            rsp = box.get_ticket (api_key=api_key)
            ticket = rsp.ticket[0].elementText        
            self.set_secure_cookie("box_ticket", ticket)
            
        box.ticket = ticket
        box.api_key = api_key
        
        box.auth_url = "http://www.box.net/api/1.0/auth/%s" % box.ticket
        return box
        