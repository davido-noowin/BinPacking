from zipzip_tree import ZipZipTree, Node, KeyType, ValType
from dataclasses import dataclass
from merge_sort import merge_sort
import sys



@dataclass
class ValPair:
    current_val: ValType
    best_val: ValType

class FirstFitZipZip(ZipZipTree):
    def __init__(self, capacity: int):
       ZipZipTree.__init__(self, capacity)


    def update_node(self, node: Node):
        if (node == None):
            return
        
        if (node.left is not None and node.right is not None):
            node.val.best_val = max(
                node.left.val.best_val,
                node.right.val.best_val,
                node.val.current_val
            )
            return

        if (node.left is not None):
            node.val.best_val = max(
                node.left.val.best_val,
                node.val.current_val
            )
            return

        if (node.right is not None):
            node.val.best_val = max(
                node.right.val.best_val,
                node.val.current_val
            )
            return
        

    def update(self, node: Node, val: ValType):
        #to_update = self.search(self.root, key)
        node.val.current_val -= val
        node.val.best_val = node.val.current_val

        # self.update_node(node)


    def update_parents(self, node: Node):
        self.update_node(node)
        if (node.left is not None):
            self.update_parents(node.left)
        
        if (node.right is not None):
            self.update_parents(node.right)

    
    def find_spot(self, root: Node, val: ValType):
        if (val <= root.val.best_val + sys.float_info.epsilon):
            if (root.left != None and val <= root.left.val.best_val + sys.float_info.epsilon):
                return self.find_spot(root.left, val)
                
            if (val <= root.val.current_val + sys.float_info.epsilon):
                return root

            if (root.right != None and val <= root.right.val.best_val + sys.float_info.epsilon):
                return self.find_spot(root.right, val)
        else:
            return None

    
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

    # makes a new bin with capacity of 1 at the beginning of the algorithm
    # key = bin number
    # val = (1, 1)
    tree.insert(0, ValPair(1, 1))

    free_space.append(1)
    for i in range(len(items)):
        # print(items[i])
        # print(tree.root.val.best_val)
        to_update = tree.in_order_update(tree.root, items[i])
        #to_update = tree.find_spot(tree.root, items[i])
        if (to_update is not None):
            remains = to_update.val.current_val - items[i]
            tree.update(to_update, items[i])
            #tree.update_parents(tree.root)
            bin = to_update.key
            free_space[bin] = remains
            assignment[i] = bin
        else:
            free_space.append(1)
            tree.insert(tree.get_size(), ValPair(1 - items[i], 1 - items[i]))
            #tree.update_parents(tree.root)
            assignment[i] = tree.get_size() - 1
            free_space[tree.get_size() - 1] = 1 - items[i]


def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    merge_sort(items)
    items.reverse()

    first_fit(items, assignment, free_space)


# '''

#bin = [0.54, 0.67, 0.46, 0.57, 0.06, 0.23, 0.83, 0.64, 0.47, 0.03, 0.53, 0.74, 0.36, 0.24, 0.07, 0.25, 0.05, 0.63, 0.43, 0.04]
#bin = [0.1, 0.8, 0.3, 0.5, 0.7, 0.2, 0.6, 0.4]
#bin = [0.7, 0.7, 0.7, 0.7, 0.3, 0.3, 0.5, 0.4]

#assign = [0] *len(bin)

#bin = [random.uniform(0.0, 0.7) for _ in range(150000)]
#assign = [0] * len(bin)
#free = []

#first_fit_decreasing(bin, assign, free)

#print(assign)
#print(free)


