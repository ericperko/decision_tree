import random

class Fold:
    def __init__(self):
        self.positives = []
        self.negatives = []

    def add_positive(self, example):
        self.positives.append(example)

    def add_negative(self, example):
        self.negatives.append(example)

    def examples(self):
        examples = self.positives + self.negatives
        examples = filter(lambda(x): None not in x, examples)
        return examples

    def __str__(self):
        return "Positives: {0}\nNegatives: {1}\n".format(self.positives, self.negatives)

def test_positive(example):
    return int(example[-1]) == 1

def stratify_folds(num_folds, data):
    random.seed(12345)
    folds = []
    for i in range(0, num_folds):
        folds.append(Fold())

    examples = []
    for i in range(1, len(data)+1):
        examples.append(data[str(i)])

    pos_examples = filter(test_positive, examples)
    neg_examples = filter(lambda(x): not test_positive(x), examples)

    random.shuffle(pos_examples)
    random.shuffle(neg_examples)

    i = 0
    while(pos_examples):
        folds[i % num_folds].add_positive(pos_examples.pop(0))
        i += 1

    i = 0
    while(neg_examples):
        folds[i % num_folds].add_negative(neg_examples.pop(0))
        i += 1

    return folds