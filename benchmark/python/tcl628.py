import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 64
m = 72
c = 54
b = 54
u = 64
gflops = a*m*c*b*u*2/1e9
A = np.empty((u,m), order='f', dtype=np.float32)
B = np.empty((a,u,b,c), order='f', dtype=np.float32)
C = np.empty((m,c,b,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,m", B, "a,u,b,c", beta, C, "m,c,b,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("um,aubc->mcba", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC