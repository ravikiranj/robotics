import node
from node import Node

# Module constants
(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Tree:
    """Class for Tree basic functionality"""
    #start __init__ 
    def __init__(self):
        self.nodes = []
    #end __init__ 

    #start get_index
    def get_index(self, position):
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index
    #end get_index

    #start create_node
    def create_node(self, name, identifier = None, parent = None):
        """Create a child node for the node indicated by the 'parent' parameter"""
        node = Node(name, identifier)
        self.nodes.append(node)
        self.__update_fpointer(parent, node.identifier, _ADD)
        node.bpointer = parent
        return node
    #end create_node

    #start show
    def show(self, position, level=_ROOT):
        queue = self[position].fpointer
        if level == _ROOT:
            print("{0} [{1}]".format(self[position].name, self[position].identifier))
        else:
            print("t"*level, "{0} [{1}]".format(self[position].name, self[position].identifier))

        if self[position].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call
    #end show
    
    #start expand_tree
    def expand_tree(self, position, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        yield position
        queue = self[position].fpointer
        while queue:
            yield queue[0]
            expansion = self[queue[0]].fpointer
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first
    #end expand_tree

    #start is_branch
    def is_branch(self, position):
        return self[position].fpointer
    #end is_branch

    #start __update_fpointer
    def __update_fpointer(self, position, identifier, mode):
        if position is None:
            return
        else:
            self[position].update_fpointer(identifier, mode)
    #end __update_fpointer

    #start __update_bpointer
    def __update_bpointer(self, position, identifier):
        self[position].bpointer = identifier
    #end __update_bpointer

    #start __getitem__
    def __getitem__(self, key):
        return self.nodes[self.get_index(key)]
    #end __getitem__

    #start __setitem__
    def __setitem__(self, key, item):
        self.nodes[self.get_index(key)] = item
    #end __setitem__

    #start __len__
    def __len__(self):
        return len(self.nodes)
    #end __len__

    #start __contains__
    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]
    #end __contains__
#end class Tree
