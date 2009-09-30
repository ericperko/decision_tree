from __future__ import division
import statlib.stats
import pdb

def test_tree(root, examples):
    result = Result()
    total_nodes = count_nodes(root)
    for example in examples:
        if None in example:
            continue
        else:
            r = test(root, example, 0)
            depth = r[1]
        result.addLabeled(example, r[0], total_nodes, depth)
    return result

def test(node, example, depth):
    if node.label is not None:
        return (node.label, depth)
    if node.test_func is None:
        depth += 1
        next_node = node.children.get(example[node.feature], None)
        if next_node:
            return test(next_node, example, depth)
        else:
            return ("1", depth-1)
    else:
        depth += 1
        next_node = node.children[node.test_func(example)]
        return test(next_node, example, depth)

def count_nodes(node):
    count = 1
    if len(node.children) > 0:
        for child in node.children:
            count += count_nodes(node.children[child])
    else:
        count = 1
    return count

def aggregate_results(results):
    accuracies = map(lambda(x): x.accuracy(), results)
    weight_accuracies = map(lambda(x): x.weightedAccuracy(), results)
    precisions = map(lambda(x): x.precision(), results)
    recalls = map(lambda(x): x.recall(), results)
    sizes = map(lambda(x): x.total_num_nodes, results)
    max_depths = map(lambda(x): x.max_depth, results)

    avg_accuracy = statlib.stats.lmean(accuracies)
    avg_wacc = statlib.stats.lmean(weight_accuracies)
    avg_prec = statlib.stats.lmean(precisions)
    avg_rec = statlib.stats.lmean(recalls)
    avg_size = statlib.stats.lmean(sizes)
    avg_max_d = statlib.stats.lmean(max_depths)
    
    print "Accuracy: {0:0.3} {1:0.3}\n".format(avg_accuracy, statlib.stats.lstdev(accuracies))
    print "Weighted Accuracy: {0:0.3} {1:0.3}\n".format(avg_wacc, statlib.stats.lstdev(weight_accuracies))
    print "Precision: {0:0.3} {1:0.3}\n".format(avg_prec, statlib.stats.lstdev(precisions))
    print "Recall: {0:0.3} {1:0.3}\n".format(avg_rec, statlib.stats.lstdev(recalls))
    print "Size: {0:0.3} {1:0.3}\n".format(avg_size, statlib.stats.lstdev(sizes))
    print "max Depth: {0:0.3} {1:0.3}".format(avg_max_d, statlib.stats.lstdev(max_depths))
    

class Result:
    def __init__(self):
        self.true_pos = 0
        self.true_neg = 0
        self.false_pos = 0
        self.false_neg = 0
        self.total_num_nodes = 0
        self.max_depth = 0

    def addLabeled(self, example, label, total_num_nodes, depth):
        self.total_num_nodes = total_num_nodes
        self.max_depth = max(depth, self.max_depth)
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

    def accuracy(self):
        num = (self.true_neg + self.true_pos)
        denom = (self.true_neg + self.true_pos + self.false_neg + self.false_pos)
        return num/denom

    def weightedAccuracy(self):
        term1 = self.true_pos/(self.true_pos + self.false_neg)
        term2 = self.true_neg/(self.true_neg + self.false_pos)
        return ((term1 + term2)/2)

    def precision(self):
        try:
            retval = self.true_pos/(self.true_pos + self.false_pos)
        except ZeroDivisionError:
            retval = 0
        return retval

    def recall(self):
        return self.true_pos/(self.true_pos + self.false_neg)
    
        
        
