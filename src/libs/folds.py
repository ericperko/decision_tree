# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="ericperk"
__date__ ="$Sep 26, 2009 10:29:53 PM$"

class Fold:
    def __init__(self):
        self.positives = []
        self.negatives = []

    def add_positive(self, example):
        self.positives.append(example)

    def add_negative(self, example):
        self.negatives.append(example)

def stratify_folds(num_folds, data):
    folds = []
    for i in range(0, num_folds):
        folds[i] = Fold()

    print data
