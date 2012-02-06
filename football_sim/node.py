import uuid

#start sanitize_id
def sanitize_id(node_id):
    return node_id.strip().replace(" ", "")
#end sanitize_id    

#Module Constants
(_ADD, _DELETE, _INSERT) = range(3)

#start class Node
class Node:
    """Class for node's basic functionality"""
    #start __init__ 
    def __init__(self, name = None, identifier = None, expanded = True):
        if(identifier == None):
            self.__identifier = str(uuid.uuid1())
        else:
            self.__identifier = sanitize_id(str(identifier))
        self.name = name
        self.expanded = expanded
        self.__bpointer = None
        self.__fpointer = []
    #end __init__

    @property
    def identifier(self):
        return self.__identifier

    @property
    def bpointer(self):
        return self.__bpointer

    @bpointer.setter
    def bpointer(self, value):
        if(value != None):
            self.__bpointer = sanitize_id(value)

    @property
    def fpointer(self):
        return self.__fpointer

    #start update_fpointer
    def update_fpointer(self, identifier, mode=_ADD):
        if(mode == _ADD):
            self.__fpointer.append(sanitize_id(identifier))
        elif(mode == _DELETE):
            self.__fpointer.remove(sanitize_id(identifier))
        elif(mode == _INSERT):
            self.__fpointer = [sanitize_id(identifier)]
    #end update_pointer

#end class Node    