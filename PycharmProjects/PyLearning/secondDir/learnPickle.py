import pickle

n = dict((("id", 2), ("name", 3)))
j = list((1, 2, 3))

with open("C:\\Users\\Dell\\PycharmProjects\\PyLearning\\savepickle.pkl", "wb") as pklfile:
    for f in range(1000):
        # this is just for increasing the size of the file for comparing the size of the data file vs pickle file
        pickle.dump(n, pklfile, True)
        pickle.dump(j, pklfile, True)
''' above we created a pickle file which contains the data n and j in sequence, 
the same order should be maintained to retrieve them. '''
with open("C:\\Users\\Dell\\PycharmProjects\\PyLearning\\savepickle.pkl", "rb") as pklfile:
    for f in range(1000):
        n1 = pickle.load(pklfile)
        j1 = pickle.load(pklfile)
        # nj = pickle.load(pklfile)

with open("C:\\Users\\Dell\\PycharmProjects\\PyLearning\\savepickle.data", "w") as datafile:
    for f in range(1000):
        datafile.write(n.__str__())
        datafile.write(j.__str__())


for f in (n1, j1):
    print(f)
    print("here")
