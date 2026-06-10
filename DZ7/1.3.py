class TreeNode:
    def __init__(self, val, size=1):
        self.val = val
        self.size = size
        self.left = None
        self.right = None

def get_size(node):
    if not node:
        return 0
    return node.size

def update_size(node):
    if node:
        node.size = get_size(node.left) + get_size(node.right) + 1

def split_bst(root, k):
    if not root:
        return None, None
    
    left_size = get_size(root.left)
    
    if left_size + 1 <= k:
        smaller, larger = split_bst(root.right, k - left_size - 1)
        root.right = smaller
        update_size(root)
        return root, larger
    else:
        smaller, larger = split_bst(root.left, k)
        root.left = larger
        update_size(root)
        return smaller, root

def build_bst(elements):
    if not elements:
        return None
    mid = len(elements) // 2
    root = TreeNode(elements[mid])
    root.left = build_bst(elements[:mid])
    root.right = build_bst(elements[mid+1:])
    update_size(root)
    return root

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

n = int(lines[0])
k = int(lines[-1])

vals = []
for i in range(1, n + 1):
    parts = list(map(int, lines[i].split()))
    vals.append(parts[1])

vals.sort()
root = build_bst(vals)

tree1, tree2 = split_bst(root, k)

val1 = tree1.val if tree1 else "Пусто"
val2 = tree2.val if tree2 else "Пусто"

print("Корни полученных деревьев:", val1, "и", val2)