from __future__ import division

from libs.dtree_helper import calcEntropy
from libs.dtree_helper import calcMaxIG

class Node():

    def __init__(self, examples, columns, use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_separating_values):
        self.children = {}
        self.test_func = None
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
            maxIG, feature, function, possible_seps = calcMaxIG(examples, columns, possible_separating_values, use_gain_ratio)
            if feature:
                pruning_value = maxIG/calcEntropy([prob_pos, prob_neg])

                self.feature = feature
                self.test_func = function

                if max_tree_depth == 0 and not use_max_depth:
                    if pruning_value <= pruning_threshhold and pruning_threshhold != 0:
                        if len(label_pos) >= len(label_neg):
                            self.label = "1"
                        else:
                            self.label = "0"
                    else:
                        new_columns = columns.copy()
                        if "continuous" in columns[self.feature+1][1]:
                            if len(possible_seps[self.feature+1]) == 0:
                                del new_columns[self.feature+1]
                            nodes_pos = filter(self.test_func, examples)
                            nodes_neg = filter(lambda(x): not self.test_func(x), examples)
                            self.children[True] = Node(nodes_pos, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                            self.children[False] = Node(nodes_neg, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                        else:
                            del new_columns[self.feature+1]
                            for value in columns[self.feature+1][1]:
                                nodes_with_value = filter(lambda(y): y[self.feature] == value, examples)
                                if len(nodes_with_value) > 0:
                                    self.children[value] = Node(nodes_with_value, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                elif max_tree_depth > 1:
                    max_tree_depth -= 1
                    new_columns = columns.copy()
                    if "continuous" in columns[self.feature+1][1]:
                        if len(possible_seps[self.feature+1]) == 0:
                            del new_columns[self.feature+1]
                        nodes_pos = filter(self.test_func, examples)
                        nodes_neg = filter(lambda(x): not self.test_func(x), examples)
                        self.children[True] = Node(nodes_pos, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                        self.children[False] = Node(nodes_neg, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                    else:
                        del new_columns[self.feature+1]
                        for value in columns[self.feature+1][1]:
                            nodes_with_value = filter(lambda(y): y[self.feature] == value, examples)
                            self.children[value] = Node(nodes_with_value, new_columns,  use_gain_ratio, pruning_threshhold, max_tree_depth, use_max_depth, possible_seps)
                elif max_tree_depth == 1 and use_max_depth:
                    if len(label_pos) >= len(label_neg):
                        self.label = "1"
                    else:
                        self.label = "0"
            else:
                if prob_pos >= prob_neg:
                    self.label = "1"
                else:
                    self.label = "0"    