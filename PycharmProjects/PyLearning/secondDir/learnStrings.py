import firstDir.testClass
import reprlib

n = 'hello world'
print(type(n))

''' Strings are represented using two methods str() and repr()'''
''' str() is a method which calls __str__() method of the object'''
''' repr() is a method which calls __repr__() method of the object'''

tc = firstDir.testClass.myClass(100, 2)
str(tc)  # str(object) return the return value of __str__ method of the object class
print(str(tc))  # to get the value
r = tc.__str__()  # calls the method explicitly
print(r)


repr(tc)  # repr(object) return the return value of __repr__ method of the object class
print(repr(tc))  # to get the value
r = tc.__repr__()  # calls the method explicitly
print(r)


''' convert a string to ascii values while retaining the unicode data as its hexadecimal values'''
mystring = "hello"
print(ascii(mystring))

mystring = "hello in chinese 你好"
print(ascii(mystring))
''' above chinese hello is converted to two unicode values retaining the ascii characters'''


print("this value is " + ord("Ã").__str__())  # convert a string to decimal value

print(chr(195))  # convert a decimal value to a string.

print(reprlib.repr(list(range(10000))))
# reprlib.repr is a handy function which only returns a sample of objects if the number is huge.
#  in this case it returned only 5 elements and showed a .... to indicate more values.
# but the below repr shows all the values whcih is pretty bad in few cases.
print(repr(list(range(10000))))
