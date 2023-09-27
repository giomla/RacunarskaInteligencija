import random
import sys

def randomTree( max_children, max_depth, curr_depth):

	if curr_depth == max_depth:
		return ""
	
	tree = "0"
	num_of_children = random.randint(0, max_children)


	for _ in range(num_of_children):
		tree += randomTree(max_children, max_depth, curr_depth + 1)
	
	tree += "1"
	return tree

def randomTreeCollection(num_trees, max_children,min_depth, max_depth):
	list = []
	for i in range(num_trees):
		r = random.randint(min_depth,max_depth)
	
		list.append(randomTree(max_children,r, 0))
	return list

def main():
    # Check if at least one argument is provided
	if len(sys.argv) !=6:
		print("Usage: python3 randomGenerator.py num_of_trees min_height max_height max_children_per_node outputfile.txt")
		return
	num_trees = int(sys.argv[1])
	min_depth = int(sys.argv[2])
	max_depth = int(sys.argv[3])
	max_children = int(sys.argv[4])
	file_path = sys.argv[5]
	tree_collection = randomTreeCollection(num_trees, max_children,min_depth,max_depth)

	with open(file_path, "w") as file:
		for tree in tree_collection:
			file.write(tree + "\n")

if __name__ == "__main__":
    main()
