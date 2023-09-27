import itertools
from tree import TreeNode , is_subtree,convert_to_tree, find_subtrees, load_from_file

def max_common_subtree(collection):
    minimal_tree = min(collection, key = lambda x: x.num_of_nodes)
    collection.remove(minimal_tree)
    subtrees1,_ = find_subtrees(minimal_tree)
    subtrees = []

    for s in subtrees1:
        subtrees.append(convert_to_tree(s))

    subtrees.sort(key = lambda x: x.num_of_nodes, reverse = True)
    
    max_tree=TreeNode("",[])
    max_num_of_nodes=1

    for s in subtrees:
        res = True
        for t in collection:
            if is_subtree(s,t)==False:
                res=False
                break
        
        if(res==True):
            max_tree=s
            max_num_of_nodes=s.num_of_nodes
            return max_tree,max_num_of_nodes
    
    return max_tree,max_num_of_nodes
