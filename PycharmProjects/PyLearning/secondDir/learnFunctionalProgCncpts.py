n = list({1, 2, 3})

print(list(map(ord, [str(n1) for n1 in n])))
# here we are running the map function on each element of n. As ord is a function of str we converted number to string.
# map function returns a map object which is basicallly a iterable.
# you have to convert to list or read thru the iterator for values.


class Trace:
    def __init__(self):
        pass

    def __call__(self, f):
        def wrap(*args, **kwargs):
            print("hello {}".format(f))
            print("args are : {}".format(*args))
            return f(*args, **kwargs)
        return wrap
# pretty complicated. Here we have defined a callable class object and its action is
# to return a function which was the input to the callable function.
# *args, **kwargs are the parameters sent to the callable class object.
# Here they are the elements of the list comprehension.


n = ['a', 'b', 'c']
nMap = map(Trace()(ord), n)
print(list(nMap))
# print(next(nMap))
# print(next(nMap))


def myord(*args):
    print(args)
    print(args[0])
    return ord(args[0]), ord(args[1])


j = ['p', 'q', 'r', 's']
nMap = map(myord, n, j)
print(next(nMap))
print(next(nMap))
print(next(nMap))

# here the function myord is taking two arguments. that's why the map function was able to use the myord function
# with two list n and j together. this will when both the lists have same number of elements.
# if there is a difference then the process would stop at the minimum number of elements among all the lists.


import functools
import operator

n = list(range(100))

print(functools.reduce(operator.add, n))
