from sys import stdin
lines = stdin.readlines()
times = lines[-1]
lines = map(lambda val: val.strip(), lines[:-1])
win = lines.count("1")
looses = lines.count("-1")
draw = lines.count("0")
print "won =", looses, " lost =", win, " draw =", draw, " total =",len(lines)