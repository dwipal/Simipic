from external.boxdotnet import BoxDotNet, BoxDotNetError
from lib.genericitems import *

from tornado.options import options


"""
Auth:
https://www.box.net/api/1.0/rest?action=get_ticket&api_key=l6ld3bydad6psc505n4p8uz5j3u3ho7h

Search
https://www.box.net/api/1.0/rest?action=search&query=shantanu&page=1&per_page=10&sort=date&direction=desc&auth_token=v4c8obcl3ifsf0kisdpd5xeygpv1l44b&params[]=nozip&params[]=onelevel&folder_id=78545944&api_key=l6ld3bydad6psc505n4p8uz5j3u3ho7h

Updates
https://www.box.net/api/1.0/rest?action=get_updates&begin_timestamp=1304229600&end_timestamp=1306908000&auth_token=v4c8obcl3ifsf0kisdpd5xeygpv1l44b&params[]=nozip&params[]=onelevel&folder_id=78545944&api_key=l6ld3bydad6psc505n4p8uz5j3u3ho7h

List:
https://www.box.net/api/1.0/rest?action=get_account_tree&auth_token=cu675thn7u0jk0vu5n9as4qyup4i8gx6&params[]=nozip&folder_id=78545944&api_key=l6ld3bydad6psc505n4p8uz5j3u3ho7h

"""

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
    
    def get_content(self, root_id, fetch_updates=False):        
        box = self._get_box_obj_with_ticket()
        token = self.authdata.get('token', None)
        
        boxtree = None
        if not token:
            raise BoxAuthError("No Token")
        
        try:
            if fetch_updates:
                print "Fetching updates..."
                boxtree = box.get_account_tree(api_key=self.api_key,
                                auth_token = self.authdata['token'], folder_id=root_id,
                                params=["nozip"])
            else:
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
            
        if fetch_updates:
            print "Files received for updates: %s"%m['folders']
            #m['files'] = m['files'][:100]
        return m

    
    def __get_root_folder(self, boxtree):
        boxtree = boxtree.tree[0]
        if boxtree.folder:
            return boxtree.folder[0]
        return None


    def __enable_share_permissions(self, boxfile, file_type=BoxFile.FILE_TYPE_FOLDER):
        box = self._get_box_obj_with_ticket()
        token = self.authdata.get('token', None)

        if boxfile['shared'] == "0":
            print "boxfile %s not shared, turning it on"%boxfile
            
            target_id = boxfile['id']
            if file_type == BoxFile.FILE_TYPE_FOLDER:
                target = 'folder'
            else:
                target= 'file'
                
                
            share_ret = box.public_share(api_key=self.api_key,
                            auth_token = self.authdata['token'],
                            target=target, target_id=target_id,
                            emails=["d2ncal@gmail.com"], message="Simipic share",
                            password="",
                            params=["nozip"])
            
    
    def __get_files(self, boxtree): 
        boxtree = boxtree.tree[0]
        rootfolder = boxtree.folder[0]
        
        self.__enable_share_permissions(rootfolder)
        
        files = []
        if 'files' in rootfolder.__dict__:
            for f in rootfolder.files[0].file:
                mtype = self.__get_media_type(f['file_name'])
                
                if mtype:
                    bf = BoxFile()
                    bf.parent_id = rootfolder['id']
                    bf.name = f['file_name']
                    bf.id = f['id']
                    bf.size = f['size']
                    bf.file_type = mtype

                    bf.large_thumbnail = f['large_thumbnail']
                    bf.preview_thumbnail = f['preview_thumbnail']
                    
                    if f['shared'] == "1":
                        bf.shared_link = f['shared_link']
                        bf.download_link = "https://www.box.net/api/1.0/download/%s/%s"%(self.authdata['token'], bf.id)
                    files.append(bf)
                    
                    if mtype == BoxFile.FILE_TYPE_VIDEO:
                        self.__enable_share_permissions(f, mtype)
                else:
                    print "Skipping non-image file %s"%f['file_name']
        else:
            print "No files in rootfolder"
        return files
    
    
    def __get_media_type(self, filename):
        filename = filename.lower()[-3:]
        if filename in ['jpg']:
            return BoxFile.FILE_TYPE_IMAGE
        elif filename in ['mov', 'mp4', 'mpg', 'avi', 'flv', "3gp", "3g2"]:
            return BoxFile.FILE_TYPE_VIDEO
    
        return None
    
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
                bf.file_type = BoxFolder.FILE_TYPE_FOLDER

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
        
