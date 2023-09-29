from tree import is_subtree, convert_to_tree, TreeNode, load_from_file
from brute_force import max_common_subtree
from simulated_annealing import simulated_annealing, simulated_annealing_with_restart
import time

tests = ["bigCollection.txt"]

for test in tests:
	
    print("Running simulated annealing on " + test + " test" )
    
    tree_collection=load_from_file(test)

    start_time = time.time()
    
    res, res_size = simulated_annealing(tree_collection,1000)
    #res,res_size = max_common_subtree(tree_collection)


    end_time = time.time() 
    print(str(res),res_size)  
    execution_time = end_time - start_time
    print("Execution time: " + str(execution_time) + "seconds\n")
    
    print("Running brute force alghorithm on " + test + " test" )
    
    tree_collection=load_from_file(test)

    start_time = time.time()
    
    #res, res_size = simulated_annealing(tree_collection,5000)
    res,res_size = max_common_subtree(tree_collection)


    end_time = time.time() 
    print(str(res),res_size)  
    execution_time = end_time - start_time
    print("Execution time: " + str(execution_time) + "seconds\n")
