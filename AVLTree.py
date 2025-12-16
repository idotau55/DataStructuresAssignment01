#id1:
#name1:
#username1:
#id2:
#name2:
#username2:


"""A class represnting a node in an AVL tree"""
from email.errors import NonASCIILocalPartDefect


class AVLNode(object):


	"""Constructor, you are allowed to add more fields. 
	
	@type key: int
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key=-1, value=-1,isRealNodeOverride = True):
		self.key = key
		self.value = value
		self.isRealNode = isRealNodeOverride
		self.left = AVLNode(isRealNodeOverride = False) if (self.isRealNode == True) else None
		self.right = AVLNode(isRealNodeOverride = False) if (self.isRealNode == True) else None
		self.parent = None
		self.height = -1
		self.oldHeight = -1 #EACH TIME WE EDIT A HEIGHT WE NEED TO REMEMBER TO PUT IT FIRST IN THE OLD HEIGHT, THIS IS FOR THE INSERT AND DELETE FUCTIONS
							# DO NOT EDIT HEIGHT MANUALLY, ONLY WITH THE setheight() funtion

	def setheight(self,newHeight):
		self.oldHeight = self.height
		self.height = newHeight


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return self.isRealNode # Need to maintain it

	def BF(self):

		#Dealing with edge cases
		if self.left is None and self.right is None: return 0

		elif self.left is not None and self.right is None:
			if self.left.height +1 != self.height: self.setheight(self.left.height +1)
			return (self.left.height +1)

		elif self.left is None and self.right is not None:
			if (1 -self.right.height) != self.height: self.setheight(1 -self.right.height)
			return (1 -self.right.height)

		else:
			b = max(self.left.height,self.right.height) + 1
			if b!= self.height:  #updating the height just in case
				self.setheight(b)
			return self.left.height - self.right.height
"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	"""
	def __init__(self,root =None):
		self.root = root
		self.max_node = None


	"""searches for a node in the dictionary corresponding to the key (starting at the root)
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def search(self, key):
		A = self.root
		e = 1
		return self.search_rec(A,key, e)

	def search_rec(self,A,key,e):
		if A is None: return None,e
		if A.key == key: return A,e
		elif A.key < key: return self.search_rec(A.right, key, e + 1)
		else: return self.search_rec(A.left, key, e + 1)

	"""searches for a node in the dictionary corresponding to the key, starting at the max
        
	@type key: int
	@param key: a key to be searched
	@rtype: (AVLNode,int)
	@returns: a tuple (x,e) where x is the node corresponding to key (or None if not found),
	and e is the number of edges on the path between the starting node and ending node+1.
	"""
	def finger_search(self, key):
		A = self.max_node()
		e =0
		return A,e


	"""inserts a new node into the dictionary with corresponding key and value (starting at the root)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def insert(self, key, val):
		e =0
		h =0
		x = AVLNode(key,val)
		if self.root is None: # Inserting the node like in normal BTS
			self.root = AVLNode(key,val)
			self.max_node = self.root
			return self.root,e,h
		A = self.root
		PARENT = None
		while A.isRealNode == True:
			PARENT = A
			if A.key < key:
				A = A.right
			else:
				A = A.left
			e+=1
		if PARENT.key < key :
			PARENT.right = x
		else:
			PARENT.left = x


		x.parent = PARENT

		h = self.Rebalance(x) #Rebalancing the Tree and saving the number of promotions it took in h

		if x.key > self.max_node.key: self.max_node = x #Maintenance on max_node
		return x,e,h # I dont understand what they want h to be and how to get it ( Think I got it :) )




	"""inserts a new node into the dictionary with corresponding key and value, starting at the max

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: (AVLNode,int,int)
	@returns: a 3-tuple (x,e,h) where x is the new node,
	e is the number of edges on the path between the starting node and new node before rebalancing,
	and h is the number of PROMOTE cases during the AVL rebalancing
	"""
	def finger_insert(self, key, val):
		return None, -1, -1


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	"""
	def delete(self, node):
		return	

	
	"""joins self with item and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: the key separting self and tree2
	@type val: string
	@param val: the value corresponding to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key,
	or the opposite way
	"""
	def join(self, tree2, key, val):
		x = AVLNode(key,val,)
		if self.root.height > key > tree2.root.height:
			B = tree2.max_node()
			while B.height < self.root.height:
				B = B.parent

			#move the subtree of B under X alongside tree2
			x.left = B
			x.right = self.root
			B.parent.right = x

			# updating the parents:
			x.parent = B.parent
			B.parent = x
			self.root.parent = x

			#update the root of the new tree
			self.root = tree2.root

		if self.root.height < key < tree2.root.height:
			B = self.max_node()
			while B.height < self.root.height:
				B = B.parent

			# move the subtree of B under X alongside out current tree
			x.right = tree2.root
			x.left = B
			B.parent.right =x

			# updating the parents:
			x.parent = B.parent
			B.parent = x
			tree2.root.parent = x

			#No need to update the root of the tree, as it remains self.root

			#in the join we already rebalanced the tree so it is a balanced AVL Tree




	"""splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: the node in the dictionary to be used for the split
	@rtype: (AVLTree, AVLTree)
	@returns: a tuple (left, right), where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, and right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		T1 = AVLTree()
		T1.root = node.left
		T2 = AVLTree()
		T2.root= node.right
		A = node
		while A.parent != None: # until we get to root
			if A.parent.right == A:
				AVL_tmp = AVLTree()
				AVL_tmp.root = A.parent.left
				T1.join(AVL_tmp, A.parent.key, A.parent.val) #if the node is a RIGHT son we join the subtree of his parent to the LEFT tree
			if A.parent.left == A:
				AVL_tmp = AVLTree()
				AVL_tmp.root = A.parent.right
				T2.join(AVL_tmp, A.parent.key, A.parent.val) #if the node is a LEFT son we join the subtree of his parent to the RIGHT tree
			A = A.parent
		return T1,T2



	
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		arr = []
		AVLTree.inorder_traversal(self.root, arr)
		return arr


	"""helper recursive function for *avl_to_array
	@returns: a list from an inorder traversal
	"""
	@staticmethod
	def inorder_traversal(root, arr=[]):
		if not root:
			return
		AVLTree.inorder_traversal(root.left, arr)
		arr.append((root.key, root.value))
		AVLTree.inorder_traversal(root.right, arr)

	"""returns the node with the maximal key in the dictionary

	@rtype: AVLNode
	@returns: the maximal node, None if the dictionary is empty
	"""
	def max_node(self):
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		A = self.root
		if (A.isRealNode != True):
			return 0
		if ( A.isRealNode == True):
			currsize = AVLTree(root=A.left).size() + AVLTree(root =A.right).size() + 1
			return currsize



	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root


	#Helping Functions


	def Rotate(self,x): #ALOT OF REPERETIVE CODE, WILL EDIT LATER (Maybe lol)
		h = 0

		if x.BF ==-2:
			#what is the BF of the RIGHT son?
			if x.right.BF == -1:
				A = x
				B = x.right
				C = x.right.right

				B.parent = A.parent
				A.left = A.right = AVLNode(isRealNodeOverride=False)
				B.left = A
				A.parent = B

				A.setHeight(-1)
				B.setHeight(1)


			if x.right.BF == 1:
				A = x
				B = x.right
				C = x.right.left

				C.parent = A.parent
				A.parent = C
				B.parent = C

				C.left = A
				C.right = B

				A.left = A.right = AVLNode(isRealNodeOverride=False)
				B.left = A.right = AVLNode(isRealNodeOverride=False)

				A.setHeight(-1)
				B.setHeight(-1)
				C.setHeight(1)

		else: #x.BF == 2
			# what is the BF of the LEFT  son?
			if x.left == -1:
				A = x
				B = x.left
				C = x.left.right

				C.parent = A.parent
				A.parent = C
				B.parent = C

				C.right = A
				C.left = B

				A.left = A.right = AVLNode(isRealNodeOverride=False)
				B.left = A.right = AVLNode(isRealNodeOverride=False)

				A.setHeight(-1)
				B.setHeight(-1)
				C.setHeight(1)

			if x.left == 1:
				A = x
				B = x.left
				C = x.left.left

				B.parent = A.parent
				A.left = A.right = AVLNode(isRealNodeOverride=False)
				B.right = A
				A.parent = B

				A.setHeight(-1)
				B.setHeight(1)
				C.setHeight(-1)


		return h
	def Rebalance(self,x):
		y = x.parent
		promotions =0
		while y is not None:
			bf = y.BF() # Will also update the height if needed
			if abs(bf) <2 and (y.height == y.oldHeight):
				break
			elif abs(bf)<2 and y.height != y.oldHeight:
				y = y.parent
				promotions+=1
			else:
				self.Rotate(y)
				break
		return promotions

