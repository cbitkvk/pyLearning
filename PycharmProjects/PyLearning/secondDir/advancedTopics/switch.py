a = int(input("enter_value"))


if a == 10:
    print("less than 10")
elif a == 20:
    print("less than 20")
elif a == 30:
    print("less than 20")
elif a == 40:
    print("less than 30")
else:
    print("raising exception, i dont know")
    print("try again")
    a = int(input("enter_value"))

# below is the cod with a switch like work around

validations = {  # here we are creating a dictionary of callables . all lambda's are callables.
    # lambda can be replaced by any other function names as well.
    # rather than writing a big if else clause that is replace by this.
    # we can just access the condition from the dictionary and that would return the
    # callable, which can be called by additional parameters if need be.
    10: lambda: print("less than 10"),
    20: lambda: print("less than 20"),
    30: lambda: print("less than 30"),
    40: lambda: print("less than 40"),
}

try:
    what_to_do = validations[a]
except KeyError as e:
    print("invalid number entered")
    print('try again')
    a = int(input("enter_value"))
else:
    what_to_do()
