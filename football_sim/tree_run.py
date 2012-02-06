import tree
from tree import Tree

if __name__ == "__main__":            
    tree = Tree()
    tree.create_node("balls", "root")
    tree.create_node("weight1", "w1", "root")
    tree.create_node("weight2", "w2", "root")
    tree.create_node("weight3", "w3", "root")
    tree.create_node("drag1", "cd1", "w2")
    tree.create_node("drag2", "cd2", "w2")
    tree.create_node("drag3", "cd3", "w2")    
    tree.show("root")
    for node in tree.expand_tree("root"):
        print(node)    
    
    
#end if    