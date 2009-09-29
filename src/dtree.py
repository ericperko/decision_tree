import pdb
import sys
import datetime

import data_parser.parser
import libs.folds
import libs.node
import libs.dtree_predict
import libs.dtree_helper

def main(args):
    problem_name, option1, option2, option3, option4 = args
    if not problem_name:
        print "You must specify a problem name."
    if int(option1) == 1:
        use_gain_ratio = False
    elif int(option1) == 2:
        use_gain_ratio = True
    else:
        print "You must specify either 1 or 2 for option 1. You specified {0}".format(option1)
    try:
        num_folds = int(option2)
    except ValueError:
        print "Option 2 must be an integer. You specified {0}".format(option2)
    if float(option3) >= 0.0 and float(option3) <= 1.0:
        pruning_threshold = float(option3)
    else:
        print "Option 3 must be a float between 0 and 1 inclusive. You specified {0}".format(option3)
    if int(option4) >= 0:
        max_tree_depth = int(option4)
    else:
        print "Option 4 must be a nonnegative integer. You specified {0}".format(option4)

    columns, data = data_parser.parser.parse(problem_name)
    stratified_folds = libs.folds.stratify_folds(num_folds, data)

    columns2 = columns.copy()
    del columns2[len(columns)-1]
    del columns2[0]

    results = []

    print datetime.datetime.now()

    for i in range(0, num_folds):
        print "Starting on fold {0}\n".format(i)
        examples = []
        for j in range(0, num_folds):
            if i != j:
                examples.extend(stratified_folds[j].examples())
        possible_separating_values = libs.dtree_helper.find_separating_values(examples, columns2)
        root = libs.node.Node(examples, columns2, use_gain_ratio, pruning_threshold, max_tree_depth, (max_tree_depth > 0), possible_separating_values)
        result = libs.dtree_predict.test_tree(root, stratified_folds[i].examples())
        results.append(result)

    print datetime.datetime.now()
    
    libs.dtree_predict.aggregate_results(results)

if __name__ == "__main__":
#    main(sys.argv[1:])
    columns = {}
    main(["ab", "1", "10", "0", "0"])
    print "Finished"
