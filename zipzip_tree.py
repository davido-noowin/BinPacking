# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar
from dataclasses import dataclass
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass
class Rank:
	geometric_rank: int
	uniform_rank: int


@dataclass
class Node:
	key: KeyType
	val: ValType
	rank: Rank
	left: Node
	right: Node


class ZipZipTree:
	def __init__(self, capacity: int):
		self.capacity = capacity
		self.size = 0
		self.height = 0
		self.root = None

	def get_random_rank(self) -> Rank:
		count = 0
		while (count <= self.height // 2):
			pass

	def insert(self, key: KeyType, val: ValType, rank: Rank = None):
		if (self.root == None):
			new_node = Node(key, val, self.get_random_rank(), None, None)
			return
		if (key < self.root.key):
			pass

	def remove(self, key: KeyType):
		pass

	def find(self, key: KeyType) -> ValType:
		pass

	def get_size(self) -> int:
		return self.size

	def get_height(self) -> int:
		pass

	def get_depth(self, key: KeyType):
		pass

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
