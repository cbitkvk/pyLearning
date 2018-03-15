def build_stack(equation):
    elem = equation.split(" ")
    elem1 = [el for el in elem if len(el)]
    return elem1


def read_data(data):
    dt = data.split("\n")
    dict = {}
    for d in dt:
        dict[d.split("|")[0]] = d.split("|")[1]
    print(dict)
    return dict


data="""vinay|100
kumar|200
sper|1000"""

evaluate = " ( vinay + kumar ) < ( sper - kumar )"

operators = ["+", "-", "/", "*", "(", ")", ">", "<", ">=", "<=", "<>", "!"]


def check_operator(data_dict, elem):
    if elem not in operators:
        try:
            return data_dict[elem]
        except Exception as p:
            print(elem)

    else:
        return elem


def calculate(data_dict, stack):
    new_exp = ""
    for elem in stack:
        new_exp = new_exp + check_operator(data_dict, elem)
    print(new_exp)
    return new_exp


def main():
    stack = build_stack(evaluate)
    print(stack)
    data_dict = read_data(data)
    new_exp = calculate(data_dict, stack)
    result = eval(new_exp)
    print(result)


if __name__ == "__main__":
    main()
