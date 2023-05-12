from zipzip_tree import ZipZipTree, Node, KeyType, ValType
from dataclasses import dataclass
import sys
import decimal
import random

@dataclass
class ValPair:
    current_val: ValType
    best_val: ValType

class FirstFitZipZip(ZipZipTree):
    def __init__(self, capacity: int):
       ZipZipTree.__init__(self, capacity)
        

    def update(self, node: Node, pair: ValPair):
        #to_update = self.search(self.root, key)
        node.val.current_val -= pair[0]
        # to_update.val.best_val = to_update.val.current_val

    
    def in_order_update(self, root: Node, val_to_be_inserted: ValType):
        if (root == None):
            return None
        else:
            left = self.in_order_update(root.left, val_to_be_inserted)
            if left:
                return left
            
            remain = root.val.current_val - val_to_be_inserted
            if (remain >= -sys.float_info.epsilon):
                return root

            right = self.in_order_update(root.right, val_to_be_inserted)
            if right:
                return right
            

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = FirstFitZipZip(capacity = len(items))
    precision = decimal.Context(prec=20)

    # makes a new bin with capacity of 1 at the beginning of the algorithm
    # key = bin number
    # val = (1, 1)
    tree.insert(0, ValPair(1, 1))

    free_space.append(1)
    for i in range(len(items)):
        candidate_key = tree.in_order_update(tree.root, items[i])

        if (candidate_key != None):
            current_best = candidate_key.val.current_val
            remains = current_best - items[i]

            first_key = candidate_key
            assignment[i] = first_key.key
            tree.update(first_key, (items[i], remains))
            free_space[first_key.key] = first_key.val.current_val

            remain = decimal.Decimal(free_space[first_key.key])
            modded = remain.quantize(decimal.Decimal('.000000000000001'), context=precision)
            free_space[first_key.key] = float(abs(modded.normalize()))
        else:
            free_space.append(1)
            tree.insert(tree.get_size(), ValPair(1, 1))
            first_key = tree.in_order_update(tree.root, items[i])
            assignment[i] = first_key.key
            tree.update(first_key, (items[i], 1 - items[i]))
            free_space[first_key.key] = first_key.val.current_val

            remain = decimal.Decimal(free_space[first_key.key])
            modded = remain.quantize(decimal.Decimal('.000000000000001'), context=precision)
            free_space[first_key.key] = float(abs(modded.normalize()))


bin = [0.1, 0.8, 0.3, 0.5, 0.7, 0.2, 0.6, 0.4]
assign = [0, 0, 0, 0, 0, 0, 0, 0]

#bin = [random.uniform(0.0, 0.7) for _ in range(150000)]
#assign = [0] * len(bin)
free = []

first_fit(bin, assign, free)

print(assign)
print(free)
