#this is an implementation of Learning with error problem of lattice based cryptography in python.

import numpy as np 
q=97
nval=20
class Alice:
	__s=None # Alice's private key
	def __init__(self,A,s,e):
		self.A=A
		self.__s=s
		self.e=e 
	def keyGen(self): #key generation
		t=[]
		for i in range(nval):
			t.append((self.A[i]*self.__s+self.e[i])%q)
		return t
	def decrypt(self,u,v): #decryption of message
		f2=(v-u*self.__s)%q
		return f2    #decrypted message
class Bob:
	__m=None #message to be encrypted
	def __init__(self, r,m):
		self.r = r
		self.__m=m 
	def encrypt(self,A,t): #encryption of message m
		u=0
		v=0
		for i in range(len(self.r)):
			u+=A[self.r[i]]
			v+=t[self.r[i]]
		v+=self.__m*int(q/2)
		u=u%q
		v=v%q
		return u,v;        # cipher text
A=np.random.randint(0,q,nval)
s=20
e=np.random.randint(1,5,nval)
r=np.random.randint(0,nval-1,int(nval/4))
m=int(input("Enter the message to be sent : 0 or 1 "))
a=Alice(A,s,e) #making an object for Alice
b=Bob(r,m) #making an object for Bob
t=a.keyGen() 
u,v=b.encrypt(a.A, t)
print("The encrypted message is: "+str(u)+" "+str(v)) 
f2=a.decrypt(u,v)
print("The decrypted message is: "+str(f2)+" and the value of q is: "+str(q)+" so")
#Testing the decrypted message
if f2>(q/2): #testing
	f2=1 
else:
	f2=0
if f2==m:
	print("The message is decrypted correctly")
else:
	print("The message is decrypted incorrectly")
