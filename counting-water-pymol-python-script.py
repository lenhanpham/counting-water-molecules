### This script uses Pymol to select water molecules, and numpy to increase the performance. Make sure that you have Pymol installed. 

from pymol import cmd 
import numpy as np

#change this value and its related parts in the names of input files to match your input file data. 
um = 557 

def calZvalueTop():
    cmd.select('seleZTop', 'resn MS2 and name SMS5 + resn MS2 and name SMS6 + resn MS2 and name SMS7 + resn MS2 and name SMS8')
    zTop = []
    cmd.iterate_state(1, 'seleZTop', 'zTop.append([x,y,z])', space=locals(), atomic=0)
    #zvalueTop = max([row[2] for row in zTop])
    zvalueTop = np.max(np.array(zTop)[:, 2])
    return zvalueTop

def calZvalueBot():
    cmd.select('seleZBot', 'resn MSB and name SMS1 + resn MSB and name SMS2 + resn MSB and name SMS3 + resn MSB and name SMS4')
    zBot = []
    cmd.iterate_state(1, 'seleZBot', 'zBot.append([x,y,z])', space=locals(), atomic=0)
    zvalueBot = np.max(np.array(zBot)[:, 2])
    return zvalueBot


def calXvalueMin():
    cmd.select('seleXmin', 'resn MSB and name SMS1 + resn MSB and name SMS2 + resn MSB and name SMS3 + resn MSB and name SMS4')
    xMin = []
    cmd.iterate_state(1, 'seleXmin', 'xMin.append([x,y,z])', space=locals(), atomic=0)
    xvalueMin = np.min(np.array(xMin)[:, 0])
    return xvalueMin 



def calXvalueMax():
    cmd.select('seleXmax', 'resn MSB and name SMS1 + resn MSB and name SMS2 + resn MSB and name SMS3 + resn MSB and name SMS4')
    xMax = []
    cmd.iterate_state(1, 'seleXmax', 'xMax.append([x,y,z])', space=locals(), atomic=0)
    xvalueMax = np.max(np.array(xMax)[:, 0])
    return xvalueMax 


def calYvalueMin():
    cmd.select('seleYmin', 'resn MSB and name SMS1 + resn MSB and name SMS2 + resn MSB and name SMS3 + resn MSB and name SMS4')
    yMin = []
    cmd.iterate_state(1, 'seleYmin', 'yMin.append([x,y,z])', space=locals(), atomic=0)
    yvalueMin = np.min(np.array(yMin)[:, 1])
    return yvalueMin 


def calYvalueMax():
    cmd.select('seleYmax', 'resn MSB and name SMS1 + resn MSB and name SMS2 + resn MSB and name SMS3 + resn MSB and name SMS4')
    yMax = []
    cmd.iterate_state(1, 'seleYmax', 'yMax.append([x,y,z])', space=locals(), atomic=0)
    yvalueMax = np.max(np.array(yMax)[:, 1])
    return yvalueMax 


def removewater():
    cmd.select('waterxl', 'resn SOL and x < %s' %(xvalueMin)) 
    cmd.remove('waterxl')
    cmd.select('waterxu', 'resn SOL and x > %s' %(xvalueMax))
    cmd.remove('waterxu')

    cmd.select('wateryu', 'resn SOL and y > %s' %(yvalueMax))
    cmd.remove('wateryu')
    cmd.select('wateryl', 'resn SOL and y < %s' %(yvalueMin))
    cmd.remove('wateryl')

    cmd.select('waterzu', 'resn SOL and z > %s' %(zvalueTop))
    cmd.remove('waterzu')
    cmd.select('waterzl', 'resn SOL and z < %s' %(zvalueBot))
    cmd.remove('waterzl')

def Average(lst):
    return sum(lst) / len(lst)

output = []

for frame in range(0,1100, 100):
    #cmd.frame(frame)
    cmd.load('extract-um%s-%s.pdb' %((um), (frame)))
    zvalueTop = calZvalueTop() 
    zvalueBot = calZvalueBot() 
    xvalueMin = calXvalueMin()
    xvalueMax = calXvalueMax()
    yvalueMin = calYvalueMin()
    yvalueMax = calYvalueMax()
    distance = zvalueTop - zvalueBot 
    removewater()
    numwater=cmd.select('innerwater', 'resn SOL and symbol O')
    output.append(numwater)
    average = Average(output)
    cmd.save('extract-um%s-%s.pdb' %((um), (frame)), 'all', -1, 'pdb')
    cmd.delete('all')
#print(output)
with open('water_molecules.csv', 'w') as f:
    #f.write(','.join(str(zcoor) for zcoor in output))
    #f.write('\n')
    f.write('{0}, {1} \n'.format(str(distance), str(average))) 
f.close()
