import pdb
def test_tree(root, examples):
    result = Result()
    for example in examples:
        if None in example:
            continue
        else:
            r = test(root, example)
            print r

def test(node, example):
    if node.label is not None:
        return node.label
    if node.test_func is None:
        next_node = node.children[example[node.feature]]
        return test(next_node, example)



class Result:
    def __init__(self):
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0

    def addLabeled(self, example, label):
        if example[-1] == "1":
            if example[-1] == label:
                self.true_pos += 1
            else:
                self.false_neg += 1
        else:
            if example[-1] == label:
                self.true_neg += 1
            else:
                self.false_pos += 1

    
        
        
