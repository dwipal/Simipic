from pymongo import Connection

class CoreData(object):
    def __init__(self):
        self.connection = Connection()
        self.database = self.connection.hellobox
        
    
    def get_user(self, username):
        users = self.database.users        
        ret = users.find_one({'username':username})
        return ret
    
    def save_user(self, userdata):
        users = self.database.users
        users.update({'username':userdata['email']}, userdata, True)
        
        
    def get_auth(self, username, service):
        authinfo  = self.database.authinfo         
        ret = authinfo.find_one({'username':username, 'service':service})
        return ret

    def add_auth(self, username, service, authdata):
        authinfo  = self.database.authinfo
        authdata['service'] = service
        authdata['username'] = username
        authinfo.update({'username':username, 'service':service}, authdata, True)
        
        
    def get_folder(self, folder_id):
        folders = self.database.folders
        ret = authinfo.find_one({'folder_id':folder_id})
        
        
    def save_folder(self, folder_id, authinfo):
        folders = self.database.folders
        
        data = {}
        
        data['folder_id'] = folder_id
        data['username'] = authinfo['username']
        
        folders.update({'folder_id':folder_id}, data, True)

