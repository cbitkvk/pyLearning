import types

superList = (k.__str__() + 'EVEN' if k % 2 == 0 else k.__str__() + 'ODD' for k in range(10))
# Here i am taking a range of values and checking if the value is even or odd.
# syntax here is
# if_clause_value if condition else else_condition_value

print(superList)
for f in superList:
    print(f + "helo")
print(type(superList))

# above consumed everything in the generator

if superList is None:
    print("none")
else:
    print("still on")

# superList is still not None even though the generator is consumed

[print(_) for _ in superList]

if isinstance(superList, types.GeneratorType):
    # type(superList) == types.GeneratorType:
    print("is generator")
else:
    print("not generator")

# checking the type of superList ( Generator)
