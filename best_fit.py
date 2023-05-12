from zipzip_tree import ZipZipTree, Node, KeyType, ValType
from dataclasses import dataclass
import sys
import decimal


class BestFitZipZip(ZipZipTree):
    def __init__(self, capacity: int):
       ZipZipTree.__init__(self, capacity)
       self.precision = decimal.Context(prec=20)


    def update(self, root: Node, key: KeyType):
        current = root
        potential = None
        min_diff = float('inf')

        while current:
            diff = current.key - key
            if -sys.float_info.epsilon <= diff < min_diff:
                min_diff = diff
                potential = current
            
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return potential

    

def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = BestFitZipZip(capacity = len(items))
    tree.precision

    # for best fit, the key is how much a bin can hold and the value is the bin number
    tree.insert(1, 0)

    free_space.append(1)

    for i in range(len(items)):
        to_update = tree.update(tree.root, items[i])
        if (to_update is not None):
            remains = to_update.key - items[i]
            if (remains >= -sys.float_info.epsilon):
                to_update.key -= items[i]
                free_space[to_update.val] = to_update.key
                assignment[i] = to_update.val
        else:
            free_space.append(1)
            ins_key = 1 - items[i]
            tree.insert(ins_key, len(free_space)-1)
            bin = tree.find(ins_key)
            free_space[bin] = ins_key
            assignment[i] = bin

    
    for i in range(len(free_space)):
        remain = decimal.Decimal(free_space[i])
        modded = remain.quantize(decimal.Decimal('.000000000000001'), context=tree.precision)
        free_space[i] = float(abs(modded.normalize()))



'''
bin = [0.1, 0.8, 0.3, 0.5, 0.7, 0.2, 0.6, 0.4]
assign = [0, 0, 0, 0, 0, 0, 0, 0]
free = []

best_fit(bin, assign, free)

print(assign)
print(free)
'''