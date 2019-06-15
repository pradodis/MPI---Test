import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import multiprocessing as mp
from math import sqrt
import time

def sqrtMillion():
    for i in range(10000000):
        a = sqrt(i)
    #print('Rodei, Oxe!!!')

def sqrtMillionPar(o):
    processes = [mp.Process(target=sqrtMillion, args=()) for i in range(10)]

    #Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

nCores = []
tSingle = []
tMulti = []
print('\33[33;1m Rodando funcao serial')
startT = time.time()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
sqrtMillion()
stopT = time.time()
singTime = stopT-startT
print(str(stopT-startT))
print('\33[0m')

print('\33[92;1m Rodando funcao paralelizada '+str(3))
startT = time.time()
sqrtMillionPar(3)
stopT = time.time()
print(str(stopT-startT))
nCores.append(3)
tSingle.append(singTime)
tMulti.append(stopT-startT)
print('\33[0m')

fig, ax = plt.subplots()
ax.plot(nCores,tSingle, nCores,tMulti)

ax.set(xlabel='Number of Cores', ylabel='Processing Time (s)',
       title='Multiprocessing Test')
ax.grid()

fig.savefig("test_100000000.png")
plt.show()