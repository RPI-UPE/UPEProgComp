import os
import sys

command = sys.argv[1]
directory = sys.argv[2]

print "command %s:: directory %s"%(command,directory)

for i in range(100):
    fullcommand = "time "+command+" "+directory+"/%d.in"%i+" >"+directory+"/%d.out"%i
    print fullcommand
    os.system(fullcommand)
