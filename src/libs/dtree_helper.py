from __future__ import division
import math
import pdb

def calcMaxIG(examples, columns, possible_separating_values, use_gain_ratio):
    maxIG = -1
    feature = None
    maxFunction = None
    for i in range(0, len(examples[0])-1):
        if i+1 not in columns:
            continue
        if i+1 in possible_separating_values:
            best_sep = None
            for sep in possible_separating_values[i+1]:
                ig, function = calcIG(i, examples, columns, use_gain_ratio, sep)
                if ig > maxIG:
                    maxIG = ig
                    feature = i
                    maxFunction = function
                    best_sep = sep
            if best_sep:
                possible_separating_values[i+1].remove(best_sep)
        else:
            ig, function = calcIG(i, examples, columns, use_gain_ratio)
            if ig > maxIG:
                maxIG = ig
                feature = i
                maxFunction = function
    if feature is None:
        pdb.set_trace()
    return (maxIG, feature, maxFunction, possible_separating_values)

def calcIG(x, examples, columns, use_gain_ratio, sep_value = None):
    prob_value_entropy_value = []
    test_function = None

    label_pos = filter(lambda(y): y[-1] == "1", examples)
    label_neg = filter(lambda(y): y[-1] == "0", examples)
    prob_pos = len(label_pos)/len(examples)
    prob_neg = len(label_neg)/len(examples)

    if "continuous" in columns[x+1][1]:
        test_function = lambda(y): y[x] <= sep_value
        value_pos_pos = filter(test_function, label_pos)
        value_neg_pos = filter(test_function, label_neg)
        value_pos_neg = filter(lambda(x): not test_function(x), label_pos)
        value_neg_neg = filter(lambda(x): not test_function(x), label_neg)
        value_pos = filter(test_function, examples)
        value_neg = filter(lambda(x): not test_function(x), examples)

        try:
            prob_pos_pos = len(value_pos_pos)/len(value_pos)
            prob_neg_pos = len(value_neg_pos)/len(value_pos)
            prob_pos_neg = len(value_pos_neg)/len(value_neg)
            prob_neg_neg = len(value_neg_neg)/len(value_neg)
        except ZeroDivisionError:
            return (-1, None)
        entropy_value_pos = calcEntropy([prob_pos_pos, prob_neg_pos])
        prob_value_entropy_value.append((len(value_pos)/len(examples), entropy_value_pos))
        entropy_value_neg = calcEntropy([prob_pos_neg, prob_neg_neg])
        prob_value_entropy_value.append((len(value_neg)/len(examples), entropy_value_neg))
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
    if use_gain_ratio:
        if "continuous" in columns[x+1][1]:
            test_function2 = lambda(y): y[x] <= sep_value
            value_pos = filter(test_function2, examples)
            value_neg = filter(lambda(x): not test_function2(x), examples)
            probs = [len(value_pos)/len(examples), len(value_neg)/len(examples)]
            h_x = calcEntropy(probs)
        else:
            probs = []
            for value in columns[x+1][1]:
                value_pos = filter(lambda(y): y[x] == value, examples)
                probs.append(len(value_pos)/len(examples))
            h_x = calcEntropy(probs)
        ig = ig/h_x
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
            separating_values[key] = []
            examples2 = map(lambda(x): (x[key-1], x[-1]), examples)
            examples2 = list(set(examples2))
            examples2.sort(key=lambda(x): x[0])
            last = examples2.pop(0)
            while(examples2):
                current = examples2.pop(0)
                if last[1] != current[1]:
                    separating_values[key].append((last[0]+current[0])/2)
                last = current
    return separating_values
