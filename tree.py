import itertools
from itertools import chain, combinations

class TreeNode:
	def __init__(self, content="", children=[]):
		self.content=content
		self.children=children
		self.num_of_nodes=1	
		self.parent=None
		self.height=None
		
		for ch in children:
			self.num_of_nodes += ch.num_of_nodes 
			ch.parent=self

		self.initialize_height()
		
	def	add_child(self, child):
		self.children.append(child)
		self.num_of_nodes += child.num_of_nodes
		child.parent = self
		self.change_size_for_parents(child.num_of_nodes)
		self.height = self.set_heights()

	def remove_child(self,child):	
		self.children.remove(child)
		self.num_of_nodes -= child.num_of_nodes       
		self.change_size_for_parents(-child.num_of_nodes )
		child.parent = None
		self.height = self.set_heights()
	
	def get_all_nodes(self):
		nodes = [self]
		for ch in self.children:
			nodes += ch.get_all_nodes()
		return nodes
		
	def change_size_for_parents(self, child_nodes):
		if self.parent!=None:
			self.parent.num_of_nodes += child_nodes
			self.parent.change_size_for_parents(child_nodes)

	def	initialize_height(self):
		if not self.children:
			self.height = 0
		else:
			self.height = max(child.height for child in self.children) + 1
	#because we recursively make the tree from the notation, the tree heights need to be set propper
	def set_heights(self):
		if(self.children==[]):
			return 0
		
		max_ch_height = 0
		for ch in self.children:
			ch.set_heights()
			max_ch_height=max(max_ch_height,ch.set_heights())

		return max_ch_height+1

	#we use the Knuth tuple representation of trees
	#swaping () with 01
	def __str__(self):
		res = "0" 
		for child in self.children:
			res += str(child)
		res +=  "1"
		return res
	#comment out for python 2.X compatibility
#	def human_readable(self):
#		return self.helper(0)

#	def helper(self, indent):
#		indent_str = " " * (indent * 4)
#		children_str = '\n'.join(child.helper(indent + 1) for child in self.children)
#		return f"{indent_str}TreeNode: {self.content}\n{children_str}"

#helper function for data instances
def convert_to_tree(notation):
	root=TreeNode("",[])
	curr_parent_node=root
	curr_node=None
	#root is procesed so we start from 1 to end-1
	for ch in notation[1:-1]:
		if ch=='0':
			curr_node=TreeNode("",[])
			curr_parent_node.add_child(curr_node)
			curr_parent_node=curr_node
		else:#==1	
			curr_parent_node=curr_parent_node.parent
	root.height = root.set_heights()
	return root

#AHU alghorithm used for isomorphism check
def is_isomorphic(tree1, tree2):
	if(tree1.num_of_nodes!=tree2.num_of_nodes):
		return False

	canonical_form1=make_canonical(tree1)	
	canonical_form2=make_canonical(tree2)

	if(canonical_form1==canonical_form2):
		return True
	else:
		return False
	
# Canonical representation of a tree orders every child by num_of_nodes
def make_canonical(tree):
	help_list = [] 
	if tree.children==[]:
		return "01"	
	else:
		for ch in tree.children:
			help_list.append(make_canonical(ch))
	
	sorted_list = sorted(help_list,key=len)
	conc_string = ''.join(sorted_list)
	return '0' + conc_string + '1'


def is_subtree(subtree, tree):
	if subtree.children == [] and tree.children == []:
		return True,1
    
	if subtree.children == []:
		return True,1

	if subtree.num_of_nodes > tree.num_of_nodes:
		return False,0
    
	if subtree.num_of_nodes == tree.num_of_nodes:
		return is_isomorphic(subtree, tree)

	if len(subtree.children) > len(tree.children):
		for child in tree.children:
			is_tree,_ = is_subtree(subtree, child)
			if is_tree:
				return True
		return False
    
	adjacency_lists = []
	for ch1 in subtree.children:
		adjacency_list = []
		for idx, ch2 in enumerate(tree.children):
			if is_subtree(ch1, ch2)==ch1.num_of_nodes:
				adjacency_list.append(idx)
		adjacency_lists.append(adjacency_list)
    
	num_left_vertices = len(subtree.children)
	num_right_vertices = len(tree.children) 
	max_matching_size,_ = max_bipartite_matching(adjacency_lists, num_left_vertices,num_right_vertices)

	return max_matching_size == num_left_vertices, max_matching_size

def max_bipartite_matching(adjacency_lists, num_left_vertices,num_right_vertices):
    pair_U = [-1] * num_left_vertices
    pair_V = [-1] *	num_right_vertices
    
    def dfs(u):
        for v in adjacency_lists[u]:
            if not seen[v]:
                seen[v] = True
                if pair_V[v] == -1 or dfs(pair_V[v]):
                    pair_U[u] = v
                    pair_V[v] = u
                    return True
        return False
    
    matching_size = 0
    for u in range(num_left_vertices):
        seen = [False] * num_right_vertices
        if dfs(u):
            matching_size += 1
    
    return matching_size


def load_from_file(filename):
	strings = []
	with open(filename, 'r') as file:
		for line in file:
			strings.append(line.strip())
            
	trees = []
	for s in strings:
		trees.append(convert_to_tree(s)) 
           
	return trees

def find_subtrees(t):

	if(t.num_of_nodes==1):
		return ["01"], ["01"]

	global_subtrees=["01"]
	all_curr = []
	unique_subtrees  = []

	for ch in t.children:
		glob, curr = find_subtrees(ch)
		all_curr.append(curr)
		global_subtrees+=glob
		#duplicate removal
		global_subtrees=list(set(global_subtrees))

	for r in range(1, len(all_curr) + 1):
		for combo in itertools.product(*all_curr):
			for selected in combinations(combo, r):
				s = ''.join(selected)
				s = '0' + s +'1'
				if s not in unique_subtrees:
					unique_subtrees.append(s)

	for s in unique_subtrees:
		if s not in global_subtrees:
			global_subtrees.append(s)

	return global_subtrees, unique_subtrees
