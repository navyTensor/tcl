import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 48
b = 48
m = 16
o = 15
n = 15
u = 15
w = 15
v = 16
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((m,o,w,n,v,u), order='f', dtype=np.float32)
B = np.empty((v,b,w,u,a), order='f', dtype=np.float32)
C = np.empty((m,n,o,a,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "m,o,w,n,v,u", B, "v,b,w,u,a", beta, C, "m,n,o,a,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("mownvu,vbwua->mnoab", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC