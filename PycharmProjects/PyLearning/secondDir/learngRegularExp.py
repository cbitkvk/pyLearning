import re
# good site for visualization of reg. https://regexper.com/


def using_match_with_lines():
    data = fh.readlines()
    all_matches = []
    line_number = 0
    for ln in data:
        line_number += 1
        ln_new = ln.strip()
        mtch = ptrn.match(ln_new)

        if mtch:
            print(mtch)
            print(line_number)
            all_matches.append(mtch)
    print(all_matches)


def using_search():
    data2 = fh.read()
    matches = ptrn.search(data2, 0, len(data2))  # ptrn.search(data2, )
    print(matches)


def piece_meal_approach():
    ln = fh.readline()
    all_matches = []
    while ln:
        mtch = ptrn.match(ln)
        all_matches.append(mtch)
        ln = fh.readline()
    print(all_matches)


def unix_grep(**kwargs):
    ln = fh.readline()
    line_number = 0
    matches = {}
    print_line_number = kwargs.get("line_number", False)
    kwargs.pop("line_number", None)
    while ln:
        line_number += 1
        ln = ln.strip()
        match = ptrn.search(ln, re.IGNORECASE, re.MULTILINE)
        if match:
            matches[line_number] = match
            if print_line_number:
                print(line_number, ":", ln)
            else:
                print(ln)
        ln = fh.readline()
    return matches


if __name__ == '__main__':
    fh = open("D:\\gitRepos\\PycharmProjects\\PyLearning\\secondDir\\learnLogging.py")
    ptrn = re.compile("import")
    grep_result = unix_grep(line_number=True, ignore_case=True)
    print(grep_result)
