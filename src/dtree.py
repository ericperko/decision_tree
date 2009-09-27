__author__="ericperk"
__date__ ="$Sep 25, 2009 10:12:55 PM$"

import sys

import data_parser.parser
import libs.folds

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
    

if __name__ == "__main__":
#    main(sys.argv[1:])
    main(["example", "1", "10", "0", "0"])
