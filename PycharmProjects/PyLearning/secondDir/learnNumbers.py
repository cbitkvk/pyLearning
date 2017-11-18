import decimal

print(decimal.Decimal(100))  # integer is converted to decimal as any default number is integer
# Here 100 is converted to fixed point decimal 100
print(decimal.Decimal(100.2))  # 100.2 is by default a float and it is converted to decimal.
# This causes conversion issues. Returned value is 100.2000000000000028421709430404007434844970703125 for 100.2


print(decimal.getcontext())
print(decimal.getcontext().__getattribute__("prec"))
decimal.getcontext().traps[decimal.FloatOperation] = True
#  above traps will make sure the decimal constructor fails when ever we use float objects for decimals
# decimal.getcontext().__setattr__()
print(decimal.getcontext())
print(decimal.Decimal('10.2'))


r = 100
print(bin(r))  # returns a binary representation of the number as a string
print(oct(r))  # returns a oct representation of the number as a string
print(hex(r))  # returns a hex representation of the number as a string


r = 0b1001  # how to assign a value in binary format. this automatically converts to decimal.
print(r)
r = 0o42  # how to assign a value in octal format. this automatically converts to decimal.
print(r)
r = 0xFA
print(r)  # how to assign a value in hexa format. this automatically converts to decimal.

# convert any number to any format

int("101", base=2)  # convert from binary to integer
int("ACF", base=16)  # convert from hexa decimal to integer
int("72", base=8)  # convert from octal to integer.

int("0o72", base=0)  # base 0 means, convert from the current base to decimal,
# if there is no info the current base value it is assumed as base 10 and no conversion is done.
# here 0o means octal. so it converts from octal to decimal
