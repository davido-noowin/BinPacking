# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import random
import math

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int

	def __lt__(self, other: Rank) -> bool:
		if (type(other) != Rank):
			return
		if (self.geometric_rank == other.geometric_rank):
			return self.uniform_rank < other.uniform_rank
		
		return self.geometric_rank < other.geometric_rank
	
	def __gt__(self, other: Rank) -> bool:
		if (type(other) != Rank):
			return
		if (self.geometric_rank == other.geometric_rank):
			return self.uniform_rank > other.uniform_rank
		
		return self.geometric_rank > other.geometric_rank
	

	def __eq__(self, other: Rank) -> bool:
		if type(other) == Rank:
			return ((self.geometric_rank == other.geometric_rank) and (self.uniform_rank == other.uniform_rank))
	

	def __le__(self, other: Rank) -> bool:
		if (type(other) != Rank):
			return
		return self < other or self == other


@dataclass
class Node:
	key: KeyType
	val: ValType
	rank: Rank
	left: Node
	right: Node

	def __str__(self):
		return f'Key: {self.key} val: {self.val} rank: {self.rank.geometric_rank}, {self.rank.uniform_rank}'


class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.root = None


	def get_random_rank(self) -> Rank:
		uniform = random.choice([i for i in range(0, int(math.log2(self.capacity)**3) - 1)])
		geo = 0
		
		while (random.choice([0, 1]) == 1):
			geo += 1

		# print(f'Geometric: {geo}, Uniform {uniform}')
		return Rank(geo, uniform)
			

	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		new_node = None
		# print(f'{self.capacity}')

		if (rank == None):
			rank = self.get_random_rank()

		new_node = Node(key, val, rank, None, None)

		# print(f'insert: {new_node}')
			
		self.size += 1
		
		current = self.root

		while ((current != None) and (rank < current.rank or (rank == current.rank and key > current.key))):
			prev = current
			current = current.left if key < current.key else current.right
		
		if (current == self.root):
			self.root = new_node
		elif (key < prev.key):
			prev.left = new_node
		else:
			prev.right = new_node

		if (current == None):
			new_node.left = None
			new_node.right = None
			return
		
		if (key < current.key):
			new_node.right = current
		else:
			new_node.left = current

		prev = new_node

		while (current != None):
			fix = prev
			if (current.key < key):
				while (True):
					if (current == None or current.key > key):
						break
					prev = current
					current = current.right
			else:
				while (True):
					if (current == None or current.key < key):
						break
					prev = current
					current = current.left

			if (fix.key > key) or (fix == new_node and prev.key > key):
				fix.left = current
			else:
				fix.right = current


	def remove(self, key: KeyType):
		to_delete = self.search(self.root, key)

		current = self.root
		while (key != current.key):
			prev = current
			current = current.left if key < current.key else current.right

		left = current.left
		right = current.right

		if (left == None):
			current = right
		elif (right == None):
			current = left
		elif (left.rank >= right.rank):
			current = left
		else:
			current = right

		if (self.root == to_delete):
			self.root = current
		elif (key < prev.key):
			prev.left = current
		else:
			prev.right = current

		while (left != None and right != None):
			if (left.rank >= right.rank):
				while (True):
					if (left == None or left.rank < right.rank):
						break
					prev = left
					left = left.right

				prev.right = right
			else:
				while (True):
					if (right == None or left.rank >= right.rank):
						break
					prev = right
					right = right.left

				prev.left = left

		self.size -= 1


	def search(self, root: Node, key: KeyType) -> Node:
		if (root == None):
			return None
		else:
			if (key == root.key):
				return root
			elif (key < root.key):
				return self.search(root.left, key)
			else:
				return self.search(root.right, key)


	def find(self, key: KeyType) -> ValType:
		return self.search(self.root, key).val


	def get_size(self) -> int:
		return self.size
	

	def dive(self, node: Node) -> int:
		if (node == None):
			return -1
		else:
			return 1 + max(self.dive(node.left), self.dive(node.right))


	def get_height(self) -> int:
		return self.dive(self.root)
	

	def depth_helper(self, root: Node, key: KeyType) -> int:
		if (root == None):
			return None
		else:
			if (key == root.key):
				return 0
			elif (key < root.key):
				return 1 + self.depth_helper(root.left, key)
			else:
				return 1 + self.depth_helper(root.right, key)


	def get_depth(self, key: KeyType) -> int:
		return self.depth_helper(self.root, key)