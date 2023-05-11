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

    
    def update(self, key: KeyType, val: ValType):
        self.in_order_update(self.root, key, val)

    
    def in_order_update(self, root: Node, key: KeyType, val_to_be_inserted: ValType):
        if (root == None):
            return None
        else:
            self.in_order_update(root.left, key, val_to_be_inserted)

            if (root.key == key):
                root.val.current_val -= val_to_be_inserted
                root.val.best_val = root.val.current_val 

            self.in_order_update(root.right, key, val_to_be_inserted)


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
        current = tree.find(count).best_val

        if (current - items[i] >= -sys.float_info.epsilon):
            assignment[i] = count # assigns this value to a bin
            tree.update(assignment[i], items[i]) # if it can go inside, update the value
            free_space[count] = tree.find(count).current_val # update free space to reflect the remaining space
        else:
            free_space.append(1)
            tree.insert(tree.get_size(), ValPair(1 - items[i], 1 - items[i]))


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