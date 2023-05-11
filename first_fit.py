from zipzip_tree import ZipZipTree, Rank, Node, KeyType, ValType
from dataclasses import dataclass
import sys
import decimal

@dataclass
class ValPair:
    current_val: ValType
    best_val: ValType

class FirstFitZipZip(ZipZipTree):
    def __init__(self, capacity: int):
       ZipZipTree.__init__(self, capacity)

    
    def ffsearch(self, root: Node, key: KeyType, pair: ValPair) -> Node:
            if (root == None):
                return None
            else:
                if (root.key == key):
                    if (root.val.best_val - pair[0] <= pair[1]):
                        root.val.best_val = pair[1]
                    return root
                elif (root.key < key):
                    if (root.val.best_val - pair[0]  <= pair[1]):
                        root.val.best_val = pair[1]
                    self.ffsearch(root.left, key, pair)
                else:
                    if (root.val.best_val - pair[0]  <= pair[1]):
                        root.val.best_val = pair[1]
                    self.ffsearch(root.right, key, pair)
        

    def update(self, key: KeyType, pair: ValPair):
        print(pair)
        to_update = self.ffsearch(self.root, key, pair)
        to_update.val.current_val -= pair[0]
        to_update.val.best_val = to_update.val.current_val
        print(to_update.val)

    
    def in_order_update(self, root: Node, val_to_be_inserted: ValType, current_best_val: ValType):
        if (root == None):
            return None
        else:
            self.in_order_update(root.left, val_to_be_inserted, current_best_val)
            
            remain = root.val.best_val - val_to_be_inserted
            if (remain >= -sys.float_info.epsilon):
                if (current_best_val < remain):
                    current_best_val = remain
                    root.val.best_val = remain
                return root.key

            self.in_order_update(root.right, val_to_be_inserted, current_best_val)


def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = FirstFitZipZip(capacity = len(items))
    precision = decimal.Context(prec=20)

    # makes a new bin with capacity of 1 at the beginning of the algorithm
    # key = bin number
    # val = (1, 1)
    tree.insert(0, ValPair(1, 1))
    count = 0 # bin number

    free_space.append(1)
    for i in range(len(items)):
        current_best = tree.find(tree.root.key).best_val

        remains = current_best - items[i]
        if (remains >= -sys.float_info.epsilon):
            first_key = tree.in_order_update(tree.root, items[i], tree.root.val.best_val)
            assignment[i] = first_key
            tree.update(first_key, (items[i], remains))
            free_space[first_key] = tree.find(first_key).current_val
        else:
            free_space.append(1)
            tree.insert(tree.get_size(), ValPair(1, 1))
            first_key = tree.in_order_update(tree.root, items[i], tree.root.val.best_val)
            assignment[i] = first_key
            tree.update(first_key, (items[i], 1 - items[i]))
            free_space[first_key] = tree.find(first_key).current_val


    for i in range(len(free_space)):
        remain = decimal.Decimal(free_space[i])
        modded = remain.quantize(decimal.Decimal('.000000000000001'), context=precision)
        free_space[i] = float(modded.normalize())


bin = [0.1, 0.8, 0.3, 0.5, 0.7, 0.2, 0.6, 0.4]
assign = [0, 0, 0, 0, 0, 0, 0, 0]
free = []

first_fit(bin, assign, free)

print(assign)
print(free)