from data_gen import  *

gen = data_generator('sentences.txt', './labels')
X, Y = next(gen)
print(len(X))
print(len(Y))