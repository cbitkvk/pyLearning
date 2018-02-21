def wordcount(line):
    wcCnt = {}
    for f in line.split(" "):
        wcCnt[f] = wcCnt.get(f,0) + 1
    return wcCnt


line = "here the function myord is taking two arguments. that's why the map function was able to use the myord function"

lines = ["here the function myord is taking two arguments. that's why the map function was able to use the myord function",
         "with two list n and j together. this will when both the lists have same number of elements",
         "if there is a difference then the process would stop at the minimum number of elements among all the lists."]

n = wordcount(line)
print(n)

p = map(wordcount, lines)
pl = list(p)
print(pl)

finalcnts = pl[0]
for l in pl[1:]:
    for key in l.keys():
        finalcnts[key] = finalcnts.get(key, 0) + l[key]

print(finalcnts)
