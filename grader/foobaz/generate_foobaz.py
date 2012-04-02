import random

def generate(fname):
  with open(fname,'w') as f:

    f.write('%d %d\n'%(random.randint(1,5), random.randint(1,5)))
    f.write('100\n')
    for i in range(100):
      f.write('%d\n'%i)


def solve(fname,foutname):
  fout = open(foutname,'w')
  with open(fname) as f:
    fline = f.readline().split(' ')
    fooint = int(fline[0])
    bazint = int(fline[1])
    val = int(f.readline())
    for i in range(val):
      inp = int(f.readline())
      if inp%fooint == 0 and inp%bazint == 0:
        fout.write('foobaz\n')
      elif inp%fooint == 0:
        fout.write('foo\n')
      elif inp%bazint == 0:
        fout.write('baz\n')
      else:
        fout.write('%d\n'%i)
  fout.close()

def solve2(fname,foutname):
  fout = open(foutname,'w')
  with open(fname) as f:
    fline = f.readline().split(' ')
    fooint = int(fline[0])
    bazint = int(fline[1])
    val = int(f.readline())
    for i in range(val):
      inp = int(f.readline())
      if inp%fooint == 0:
        fout.write('foo\n')
      elif inp%bazint == 0:
        fout.write('baz\n')
      else:
        fout.write('%d\n'%i)
  fout.close()

for d in range(5):
  generate('%d.in'%d)
  solve('%d.in'%d,'%d.out'%d)
  solve2('%d.in'%d,'%d_wrong.out'%d)

