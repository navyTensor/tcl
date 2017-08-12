import tcl
import numpy as np
import time
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
a = 25
c = 24
b = 25
m = 25
n = 24
u = 25
v = 25
gflops = a*c*b*m*n*u*v*2/1e9
A = np.empty((n,v,m,u), order='f', dtype=np.float32)
B = np.empty((c,b,u,v,a), order='f', dtype=np.float32)
C = np.empty((n,m,c,a,b), order='f', dtype=np.float32)
tcl.randomNumaAwareInit(A)
tcl.randomNumaAwareInit(B)
tcl.randomNumaAwareInit(C)
alpha = 1.0
beta = 0.0
s = time.time()
tcl.tensorMult( alpha, A, "n,v,m,u", B, "c,b,u,v,a", beta, C, "n,m,c,a,b" )
timeTCL = time.time() - s
s = time.time()
C_ = np.einsum("nvmu,cbuva->nmcab", A, B)
timeNP = time.time() - s
print "%.2f GFLOPS %.2f GFLOPS %.2fx"%( gflops/timeTCL, gflops/timeNP, timeNP/ timeTCL)
#if( not tcl.equal(C, C_) ):
#    print "validation:" + FAIL + " failed!!!" + ENDC