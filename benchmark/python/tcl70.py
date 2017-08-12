import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 32
u = 32
m = 24
w = 32
v = 32
gflops = a*u*m*w*v*2/1e9
A = np.empty((m,v,u,w), order='f', dtype=np.float32)
B = np.empty((u,a,v,w), order='f', dtype=np.float32)
C = np.empty((m,a), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,v,u,w", B, "u,a,v,w", beta, C, "m,a" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mvuw,uavw->ma", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC