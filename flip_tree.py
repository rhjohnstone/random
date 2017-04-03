def flip(tree):
    tree = tree[::-1]
    for i in xrange(2):
        if isinstance(tree[i], (int, long)):
            continue
        else:
            tree[i] = flip(tree[i])
    return tree

tree1 = [[1, 2], [3, [4, 5]]]
tree2 = [1, [2, 3]]
tree3 = [[1, [2, 3]], [[4, 5], 6]]

print flip(tree1)
print flip(tree2)
print flip(tree3)