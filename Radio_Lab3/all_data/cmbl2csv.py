import numpy as np
import sys

#print sys.stdin.read()
#fname = 'natlogansam_radiolab2/sun1.cmbl'
#fname = sys.stdin.read()
#print fname
fnames = []
for line in sys.stdin:
    #print line
    fnames.append(line.rstrip('\n'))
print fnames
for fname in fnames:
    data1 = []
    with open(fname, 'r') as f:
        for line in f:
            if '<' in line:
                continue
            data1.append(float(line.rstrip('\n')))
    f.close()
    n = len(data1)/2
    data2 = np.zeros([n,2])
    for i in range(n):
        data2[i,0] = data1[i]
        data2[i,1] = data1[i+n]
    np.savetxt(fname.rstrip('.cmbl')+'_new.csv',data2,delimiter=',')

