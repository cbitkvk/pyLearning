import firstDir.firstClass
import sys

print(sys.path)
print(locals())
''' Here python already added the current project ( PyLearning) in sys.path , 
that's why we could directly inport the other package firstDir directly.
'''

''' output of locals is below 
{'__name__': '__main__', '__doc__': None, '__package__': None, 
'__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x00000221D7424F28>, '__spec__': None,
 '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 
 '__file__': 'C:/Users/Dell/PycharmProjects/PyLearning/secondDir/firstProg.py', 
 '__cached__': None, 
 'firstDir': <module 'firstDir' from 'C:\\Users\\Dell\\PycharmProjects\\PyLearning\\firstDir\\dummy.py'>, 
 'sys': <module 'sys' (built-in)>}
which explains the same
'''

firstInst = firstDir.firstClass.HelloWorld()
''' above i created an object called firstInst. This invokes the __init__ method of HelloWorld 
but it does not pass any values which causes it to set to default values'''
print(firstInst())
''' here i am trying to call the instance of the class Hello called firstInst,
this calls the function __call__ defined in HelloWorld class'''

print(firstInst)
''' here i am just trying to print the object, this causes it to invoke __str__ of the class
'''

print(callable(firstInst))
