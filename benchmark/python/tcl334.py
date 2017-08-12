import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 144
m = 12
o = 12
n = 12
p = 16
u = 12
v = 16
gflops = a*m*o*n*p*u*v*2/1e9
A = np.empty((v,o,n,p,u,m), order='f', dtype=np.float32)
B = np.empty((a,u,v), order='f', dtype=np.float32)
C = np.empty((p,m,n,o,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "v,o,n,p,u,m", B, "a,u,v", beta, C, "p,m,n,o,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("vonpum,auv->pmnoa", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC