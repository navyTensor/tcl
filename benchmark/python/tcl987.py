import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 64
b = 64
m = 16
o = 18
n = 18
u = 16
w = 18
v = 16
gflops = a*b*m*o*n*u*w*v*2/1e9
A = np.empty((u,o,w,n,v,m), order='f', dtype=np.float32)
B = np.empty((v,b,a,w,u), order='f', dtype=np.float32)
C = np.empty((m,a,n,b,o), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "u,o,w,n,v,m", B, "v,b,a,w,u", beta, C, "m,a,n,b,o" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("uownvm,vbawu->manbo", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC