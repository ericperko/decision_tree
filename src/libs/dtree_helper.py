from __future__ import division
import math

def calcMaxIG(examples, columns):
    maxIG = 0
    feature = None
    for i in range(0, len(examples[0])-1):
        ig, function = calcIG(i, examples, columns)
        if ig > maxIG:
            maxIG = ig
            feature = i
    return i

def calcIG(x, examples, columns):
    prob_value_entropy_value = []
    test_function = None

    label_pos = filter(lambda(y): y[-1] == "1", examples)
    label_neg = filter(lambda(y): y[-1] == "0", examples)
    prob_pos = len(label_pos)/len(examples)
    prob_neg = len(label_neg)/len(examples)

    if "continuous" in columns[x+1][1]:
        pass 
    else:
        for value in columns[x+1][1]:
            value_pos_pos = filter(lambda(y): y[x] == value, label_pos)
            value_neg_pos = filter(lambda(y): y[x] == value, label_neg)
            value_pos = filter(lambda(y): y[x] == value, examples)

            prob_pos_pos = len(value_pos_pos)/len(value_pos)
            prob_neg_pos = len(value_neg_pos)/len(value_pos)
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
        
    