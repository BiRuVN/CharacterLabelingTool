import os
import numpy as np
import re
from collections import defaultdict


def data_generator(data_file, label_folder, batch_num=8):

    with open(data_file, 'r') as f:
        sentences = [s.lower() for s in f.read().split('\n')]
        f.close()

    labels = []
    for txt in os.listdir(label_folder):
        with open(label_folder + '/' + txt, 'r') as f:
            l = list(f.read())
            labels.append(l)
            f.close()

    len_total = len(sentences)
    print('There are total {} sentences'.format(str(len_total)))

    X = []
    Y = []
    for batch in range(int(len_total/batch_num)):
        for i in range(batch_num):
            x = encode_sentence(sentences[batch*8+i])
            x = x + [create_oh(batch*8+i)]*(256-len(x))
            X.append(np.array(x))
            y = labels[batch*8+i]
            y = y + [0]*(256-len(y))
            Y.append(y)
        yield X, Y


def create_oh(index):
    oh = [0]*max_len

    if index == -1:
        return oh

    oh[index] = 1
    return oh

def encode_sentence(sent):
    return [data_characters[c] for c in sent]

capital_included = False
if capital_included:
    str_characters = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNNOPQRSTUVXYZ\
ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ\
ẠẢÃÀÁÂẬẦẤẨẪĂẮẰẶẲẴÓÒỌÕỎÔỘỔỖỒỐƠỜỚỢỞỠÉÈẺẸẼÊẾỀỆỂỄÚÙỤỦŨƯỰỮỬỪỨÍÌỊỈĨÝỲỶỴỸĐ\
0123456789,.?!@$&/()[]{}+\'\""
else:
    str_characters = "abcdefghijklmnopqrstuvxyzạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ\
0123456789,.?!@$&/()[]{}+\'\""

vocabulary = [x for x in str_characters]
max_len = len(vocabulary)
one_hot_vocab = [np.array(create_oh(i)) for i in range(max_len)]
data_characters = dict(zip(vocabulary, one_hot_vocab))
data_characters = defaultdict(lambda: [0]*max_len, data_characters)

if __name__ == "__main__":
    gen = data_generator('sentences.txt', './labels')
    X, Y = next(gen)
    print(len(X))
    print(len(Y))



