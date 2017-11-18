n = (1, 2, 3)
print(type(n))
print(dir(n))
''' above, n is a tuple'''
n = n.__iter__()  # Here we are converting a tuple to a tuple_iterator

print(n.__next__())

n = [1, 2, 3]
print(type(n))
print(dir(n))
''' above, n is a list'''

n = range(3)
print(type(n))
print(dir(n))
''' above, n is a range class instance '''

n = (k for k in range(3))
print(type(n))
print(dir(n))
''' above, n is a generator'''
print(n.__next__())
print(n.__next__())
print(n.__next__())
print(n.__next__())
''' here i am getting the next value from the generator, it works fine for 0, 1, 2 
but later it fails as the genrator does not have any more values'''
