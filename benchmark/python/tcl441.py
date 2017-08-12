import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 24
m = 24
o = 24
n = 24
p = 24
u = 24
gflops = a*m*o*n*p*u*2/1e9
A = np.empty((a,u), order='f', dtype=np.float32)
B = np.empty((o,u,m,n,p), order='f', dtype=np.float32)
C = np.empty((a,p,n,o,m), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "a,u", B, "o,u,m,n,p", beta, C, "a,p,n,o,m" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("au,oumnp->apnom", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC