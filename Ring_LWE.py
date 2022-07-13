# this is an implementation of key exchange mechanism in public key cryptography based on ring learning with error problem.

import numpy as np
from numpy.polynomial import polynomial as p


n = 1024
qval = 32

q = 2**qval-1 # generating a prime number

xN_1 = [1] + [0] * (n-1) + [1] # (x^n + 1)


def gen_poly(n,q):
    global xN_1
    l = 0 #Mean value for gaussian distribution
    poly = np.floor(np.random.normal(l,size=(n)))
    return poly

class Alice:
	_sA=None
	def __init__(self,A,sA,eA):
		self.A=A
		self.__sA=sA
		self.eA=eA 
	def KeyGen(self):
		bA = p.polymul(self.A,self.__sA)%q
		bA = p.polyadd(bA,self.eA)%q
		return bA
	def genShared(self,bB):
		sharedAlice = np.floor(p.polymul(self.__sA,bB)%q)
		sharedAlice = np.floor(p.polydiv(sharedAlice,xN_1)[1])%q 
		return sharedAlice
class Bob:
	_sB=None
	def __init__(self,A,sA,eA):
		self.__sB=sB
		self.A=A
		self.eB=eB 
	def KeyGen(self):
		bB = p.polymul(self.A,self.__sB)%q
		bB = p.polyadd(bB,self.eB)%q
		return bB
	def genShared(self,bA):
		sharedBob = np.floor(p.polymul(self.__sB,bA)%q)
		sharedBob = np.floor(p.polydiv(sharedBob,xN_1)[1])%q
		return sharedBob



#Generate A which is the shared polynomial
A = np.floor(np.random.random(size=(n))*q)%q
A = np.floor(p.polydiv(A,xN_1)[1])
print("n: ",n)
print("A: ",len(A),"|",A)

#Alice (Secret & Error)
sA = gen_poly(n,q)
eA = gen_poly(n,q)
a=Alice(A,sA,eA)
bA=a.KeyGen()


#Bob (Secret and Error)
sB = gen_poly(n,q)
eB = gen_poly(n,q)
b=Bob(A,sB,eB)
bB=b.KeyGen()


#Shared Secret
sharedAlice=a.genShared(bB)
sharedBob=b.genShared(bA)
print("Before error rounding :")
print("Shared key of ALice: ",sharedAlice)
print("Shared key of Bob: ",sharedBob)


#Error Rounding
u = np.array([0] * n)
i = 0
# this error rounding can be done by any one of bA or bB
while (i < len(u)):
	if (len(bA) <= i):
		break
	if (int(bA[i]/(q/4)) == 0): u[i] = 0
	elif (int(bA[i]/(q/2)) == 0): u[i] = 1
	elif (int(bA[i]/(3*q/4)) == 0): u[i] = 0
	elif (int(bA[i]/(q)) == 0): u[i] = 1
	else:
		print("error! (1)")
	i+=1

#Bob
i = 0
while (i < len(u)):
	#Region 0 (0 --- q/4 and q/2 --- 3q/4)
	if (u[i] == 0):
		if (sharedBob[i] >= q*0.125 and sharedBob[i] < q*0.625): #middle half region of 0
			sharedBob[i] = 1
		else:
			sharedBob[i] = 0


	#Region 1 (q/4 --- q/2 and 3q/4 --- q)
	elif (u[i] == 1):
		if (sharedBob[i] >= q*0.875 and sharedBob[i] < q*0.375): #boundary region of 1
			sharedBob[i] = 0
		else:
			sharedBob[i] = 1

	else:
		print("error! (2)")

	i += 1

#Alice
i = 0
while (i < len(u)):
	#Region 0 (0 --- q/4 and q/2 --- 3q/4)
	if (u[i] == 0):
		if (sharedAlice[i] >= q*0.125 and sharedAlice[i] < q*0.625):
			sharedAlice[i] = 1
		else:
			sharedAlice[i] = 0


	#Region 1 (q/4 --- q/2 and 3q/4 --- q)
	elif (u[i] == 1):
		if (sharedAlice[i] >= q*0.875 and sharedAlice[i] < q*0.375):
			sharedAlice[i] = 0
		else:
			sharedAlice[i] = 1

	else:
		print("error! (3)")
	i += 1


print("After error rounding: ")
print("Shared Secret Alice:",len(sharedAlice),"|",sharedAlice)
print("Shared Secret Bob:",len(sharedBob),"|",sharedBob)

print("\n--Verification--")
i = 0
flag=0
while (i < len(sharedBob)):
	if (sharedAlice[i] != sharedBob[i]):
		print("Error at index",i)
		flag=1
	i+=1
if flag==0:
	print("Both the shared keys are verified successfully: Have no errors and are eqaul")
else:
	print("Both the shared keys are verified successfully: Have listed errors and are not eqaul")
