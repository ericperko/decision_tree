from __future__ import division
import math
import pdb

def calcMaxIG(examples, columns):
    maxIG = 0
    feature = None
    maxFunction = None
    for i in range(0, len(examples[0])-1):
        if i+1 not in columns:
            continue
        ig, function = calcIG(i, examples, columns)
        if ig > maxIG:
            maxIG = ig
            feature = i
            maxFunction = function
    return (maxIG, feature, maxFunction)

def calcIG(x, examples, columns):
    prob_value_entropy_value = []
    test_function = None

    label_pos = filter(lambda(y): y[-1] == "1", examples)
    label_neg = filter(lambda(y): y[-1] == "0", examples)
    prob_pos = len(label_pos)/len(examples)
    prob_neg = len(label_neg)/len(examples)

    if "continuous" in columns[x+1][1]:
        return (-1, None)
    else:
        for value in columns[x+1][1]:
            value_pos_pos = filter(lambda(y): y[x] == value, label_pos)
            value_neg_pos = filter(lambda(y): y[x] == value, label_neg)
            value_pos = filter(lambda(y): y[x] == value, examples)

            try:
                prob_pos_pos = len(value_pos_pos)/len(value_pos)
                prob_neg_pos = len(value_neg_pos)/len(value_pos)
            except ZeroDivisionError:
                continue
            entropy_value_pos = calcEntropy([prob_pos_pos, prob_neg_pos])
            prob_value_entropy_value.append((len(value_pos)/len(examples), entropy_value_pos))
    entropy_y_given_x = 0
    for prob, entropy in prob_value_entropy_value:
        entropy_y_given_x += prob * entropy

    entropy_y = calcEntropy([prob_pos, prob_neg])

    ig = entropy_y - entropy_y_given_x
    return (ig, test_function)
    
        
def calcEntropy(probabilities):
    return sum(map(calcLog, probabilities))

def calcLog(p):
    if p == 0 or math.isnan(p):
        return 0
    else:
        return -1*p*math.log(p, 2)

def find_separating_values(examples, columns):
    separating_values = {}
    for key in columns:
        if "continuous" in columns[key][1]:
            examples2 = map(lambda(x): (x[key-1], x[-1]), examples)
            examples2 = list(set(examples2))
            examples2.sort(key=lambda(x): x[0])
            print examples2
        
    