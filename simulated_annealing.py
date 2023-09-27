import random
import math
from copy import deepcopy
from tree import TreeNode,is_subtree, convert_to_tree,load_from_file, find_subtrees

def initialize(collection):
    max_height_tree = min(collection,key= lambda node : node.height)
    max_height = max_height_tree.height
    max_num_of_nodes = min(collection, key= lambda node: node.num_of_nodes).num_of_nodes
    return TreeNode("",[]), max_height, max_num_of_nodes

def generate_random_subtree(tree):
    if tree.children==[]:
        return
   
    for child in tree.children:
        #heuristicaly here could be anything, experimentaly inclined to this
        #0.25- 0.35 - 0.5 gave best results
        if random.random() < 0.27:
            tree.remove_child(child)
        else:
            generate_random_subtree(child)

def generate_random_subtree1(tree, curr_level, max_level):

    if tree.children==[] or curr_level==max_level:
        return 

    for child in tree.children:

        if random.random() < 0.3 :
            tree.remove_child(child)
        else:
            generate_random_subtree1(child, curr_level+1, max_level)

def generate_random_subtree1(tree, curr_level, max_level):

    if tree.children==[] or curr_level==max_level:
        return 

    for child in tree.children:

        if random.random() < 0.3 :
            tree.remove_child(child)
        else:
            generate_random_subtree1(child, curr_level+1, max_level)


def initialize1(collection):
    max_height_tree = min(collection,key= lambda node : node.height)
    max_height = max_height_tree.height
    min_tree= min(collection, key= lambda node: node.num_of_nodes)
    max_nodes=min_tree.num_of_nodes
    rand_sub=deepcopy(min_tree)
    generate_random_subtree1(rand_sub,0, max_height)
    return rand_sub,max_height,max_nodes

def initialize2(collection):
    max_height_tree = min(collection,key= lambda node : node.height)
    max_height = max_height_tree.height
    min_tree= min(collection, key= lambda node: node.num_of_nodes)
    max_nodes=min_tree.num_of_nodes
    return min_tree,max_height,max_nodes

def calc_solution_value(solution, collection):
    for t in collection:
        if is_subtree(solution, t)==False:
           return 0 
    return solution.num_of_nodes

def make_small_change(solution,max_nodes,max_height,p):
    solution=deepcopy(solution)

    rand_choice =random.randrange(3)
    all_nodes= solution.get_all_nodes()
    rand_node = random.choice(all_nodes)

    if rand_choice==0:
        #add a node to the random node
        if solution.num_of_nodes < max_nodes:
            rand_node.add_child(TreeNode("",[]))
        else:
            rand_choice=1
    if rand_choice==1 and random.random()>p:
        #remove node
        if rand_node.parent != None:
            rand_node.parent.remove_child(rand_node)
    	#add all to a parent node
    if rand_choice==2:
        solution = TreeNode("",[solution])

    return solution

def make_small_change1(solution,max_nodes,max_height,p):
    solution=deepcopy(solution)

    rand_choice =random.randrange(2)
    all_nodes= solution.get_all_nodes()
    rand_node = random.choice(all_nodes)

    if rand_choice==0:
        #add a node to the random node
        if solution.num_of_nodes < max_nodes:
            node1 =TreeNode("",[])
            rand_node.add_child(node1)
        else:
            rand_choice=1
    if rand_choice==1:
        #remove node
        if rand_node.parent != None:
            rand_node.parent.remove_child(rand_node)

    return solution

def make_small_change2(solution, max_nodes,max_height,p):    
    solution=deepcopy(solution)

    rand_choice =random.randrange(3)
    all_nodes= solution.get_all_nodes()
    rand_node = random.choice(all_nodes)

    if rand_choice==0 and random.random()>p:
        #remove node
        if rand_node.parent != None:
            rand_node.parent.remove_child(rand_node)
    
    if rand_choice==1:
        #add a node to the random node
        if solution.num_of_nodes < max_nodes:
            rand_node.add_child(TreeNode("",[]))
        else:
            rand_choice=1  

    return solution

def simulated_annealing(collection, max_iters):

    solution,max_height,max_num_of_nodes = initialize1(collection)
    value = calc_solution_value(solution,collection)
    best_solution = deepcopy(solution)
    best_value = value
    
    for i in range(1, max_iters):
        #p = math.log(2) / math.log(i+1) #1
        #p = 1/ math.log(i+1)           #2 
        p = 1 / (i+1) ** 0.5          #3
        new_solution = make_small_change1(solution,max_num_of_nodes,max_height,p)
        new_value = calc_solution_value(new_solution, collection)
        
        if new_value > value:
            value = new_value
            solution = deepcopy(new_solution)
            if new_value > best_value:
                best_value = new_value
                best_solution = deepcopy(new_solution)
        else:
            q = random.random()
            if q < p:
                value = new_value
                solution = deepcopy(new_solution)
                
    return best_solution, best_value

def simulated_annealing_with_restart(collection, max_iters):

    solution,max_height,max_num_of_nodes = initialize1(collection)
    value = calc_solution_value(solution,collection)
    best_solution = deepcopy(solution)
    best_value = value
    
    for i in range(1, max_iters):
        #p = math.log(2) / math.log(i+1) #1
        #p = 1/ math.log(i+1)           #2 
        p = 1 / (i+1) ** 0.5           #3
        new_solution = make_small_change1(solution,max_num_of_nodes,max_height,p)
        new_value = calc_solution_value(new_solution, collection)
        
        if new_value > value:
            value = new_value
            solution = deepcopy(new_solution)
            if new_value > best_value:
                best_value = new_value
                best_solution = deepcopy(new_solution)
        else:
            q = random.random()
            if q < p and new_value!=0:
                value = new_value
                solution = deepcopy(new_solution)

    if(best_value==0):
        best_solution,best_value=simulated_annealing(collection,max_iters)

    return best_solution, best_value

