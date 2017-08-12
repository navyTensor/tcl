import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 15
b = 16
m = 16
o = 16
n = 16
u = 16
v = 16
gflops = a*b*m*o*n*u*v*2/1e9
A = np.empty((u,b,a,v), order='f', dtype=np.float32)
B = np.empty((v,n,o,u,m), order='f', dtype=np.float32)
C = np.empty((b,m,a,o,n), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,b,a,v", B, "v,n,o,u,m", beta, C, "b,m,a,o,n" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("ubav,vnoum->bmaon", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC