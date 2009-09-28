from __future__ import division
import pdb

from libs.dtree_helper import calcEntropy
from libs.dtree_helper import calcMaxIG

class Node():
    def __init__(self, examples, columns, use_gain_ratio, pruning_threshhold, max_tree_depth):
        self.children = {}
        self.test = None
        self.feature = None
        self.label = None

        label_pos = filter(lambda(y): y[-1] == "1", examples)
        label_neg = filter(lambda(y): y[-1] == "0", examples)

        prob_pos = len(label_pos)/len(examples)
        prob_neg = len(label_neg)/len(examples)

        if len(label_pos) == 0 and len(label_neg) > 0:
            self.label = "0"
        elif len(label_pos) > 0 and len(label_neg) == 0:
            self.label = "1"
        elif len(columns) == 0:
            if prob_pos >= prob_neg:
                self.label = "1"
            else:
                self.label = "0"
        else:
            if not use_gain_ratio:
                maxIG, feature, function = calcMaxIG(examples, columns)
                pruning_value = maxIG/calcEntropy([prob_pos, prob_neg])
            else:
                pass

            self.feature = feature
            self.test = function

            if max_tree_depth == 0:
                if pruning_value <= pruning_threshhold:
                    if len(label_pos) >= len(label_neg):
                        self.label = "1"
                    else:
                        self.label = "0"
                else:
                    new_columns = columns.copy()
                    del new_columns[self.feature+1]
                    if "continuous" in columns[self.feature+1][1]:
                        pass
                    else:
                        for value in columns[self.feature+1][1]:
                            nodes_with_value = filter(lambda(y): y[self.feature] == value, examples)
                            self.children[value] = Node(nodes_with_value, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth)
                
