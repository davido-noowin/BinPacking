from zipzip_tree import ZipZipTree, Node, KeyType, ValType
from dataclasses import dataclass
from merge_sort import merge_sort
import sys
import random


class BestFitZipZip(ZipZipTree):
    def __init__(self, capacity: int):
       ZipZipTree.__init__(self, capacity)


    def update(self, root: Node, key: KeyType):
        current = root
        potential = None
        min_diff = float('inf')

        while current:
            diff = current.key[0] - key
            if (-sys.float_info.epsilon <= diff <= min_diff):
                min_diff = diff
                potential = current
            
            if key == current.key[0]:
                return current
            elif key < current.key[0]:
                current = current.left
            else:
                current = current.right

        return potential

    
def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = BestFitZipZip(capacity = len(items))

    # for best fit, the key is how much a bin can hold and the value is the bin number
    tree.insert([1, 0], 0)

    free_space.append(1)

    for i in range(len(items)):
        to_update = tree.update(tree.root, items[i])
        if (to_update is not None):
            remains = to_update.key[0] - items[i]
            if (remains >= -sys.float_info.epsilon):
                bin = to_update.val
                tree.remove(to_update.key)
                free_space[bin] = remains
                assignment[i] = bin
                if (remains > 0 + sys.float_info.epsilon):
                    tree.insert([remains, bin], bin)
        else:
            free_space.append(1)
            ins_key = 1 - items[i]
            tree.insert([ins_key, len(free_space)-1], len(free_space)-1)
            bin = len(free_space) - 1
            free_space[bin] = ins_key
            assignment[i] = bin


def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    merge_sort(items)
    items.reverse()

    best_fit(items, assignment, free_space)


def slow_best_fit(items: list[float], assignment: list[int], free_space: list[float]):
        for item in items:
            bin_index = -1
            min_space = float('inf')
            for i in range(len(free_space)):
                if item <= free_space[i] + sys.float_info.epsilon and free_space[i] < min_space:
                    bin_index = i
                    min_space = free_space[i]
            if bin_index == -1:
                # Create a new bin for the item
                assignment.append(len(free_space))
                free_space.append(1.0 - item)
            else:
                assignment.append(bin_index)
                free_space[bin_index] -= item


'''
#bin = [0.54, 0.67, 0.46, 0.57, 0.06, 0.23, 0.83, 0.64, 0.47, 0.03, 0.53, 0.74, 0.36, 0.24, 0.07, 0.25, 0.05, 0.63, 0.43, 0.04]
#bin = [random.uniform(0.0, 1.0) for _ in range(200000)]
bin = [0.7, 0.7, 0.7, 0.7, 0.3, 0.3, 0.5, 0.4]
assign = [0] * len(bin)
free = []


assign1 = []
free1 = []

#slow_best_fit(sorted(bin, reverse=True), assign1, free1)
best_fit(bin, assign, free)
#print('done')

print(assign == assign1)
print(free == free1)
print(assign)
print(free)


#print(assign1)
#print(free1)
'''
