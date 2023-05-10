from zipzip_tree import ZipZipTree, Rank

def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = ZipZipTree(capacity = len(items))