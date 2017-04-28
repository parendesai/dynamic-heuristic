from sys import stdin
def makeInt(st):
	# print st
	return map(int, st.strip().split())
m = stdin.readlines()

m = map(makeInt, m)

def md27(n):
	return n%27

def modArr(arr):
	return map(md27, arr)

m=map(modArr, m)
for i in m:
	print i