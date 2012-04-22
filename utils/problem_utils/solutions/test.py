import sys

f = open(sys.argv[1])
num = int(f.readline())
for i in range(num):
    print f.readline().strip()
