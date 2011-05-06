class AbstractBoxItem(object):
    FILE_TYPE_IMAGE = 1
    FILE_TYPE_VIDEO = 2
    FILE_TYPE_FOLDER = 3


    name = ""
    id = ""
    parent_id = ""
    
    def __init__(self):
        pass
    
class BoxFolder(AbstractBoxItem):
    filecount = 0
    file_type = AbstractBoxItem.FILE_TYPE_FOLDER
    def __init__(self):
        pass
     

class BoxFile(AbstractBoxItem):
    file_type = None
    
    
    def __init__(self):
        pass



