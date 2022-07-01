#this is an implementation of Learning with error problem of lattice based cryptography in python.

import numpy as np 
q=13
#matrix multiplication
def modular_mult(m1,m2):
	res=(m1.dot(m2))%q
	return res
#matrix addition
def modular_add(m1,m2):
	res=(m1+m2)%q
	return res
#matrix subtraction
def modular_sub(m1,m2):
	res=(m1-m2)%q
	return res
class Alice:
	__s=None # Alice's private key
	def __init__(self,A,s,e):
		self.A=A
		self.__s=s
		self.e=e 
	def keyGen(self): #key generation
		t=modular_mult(self.A,self.__s)
		t=modular_add(t,self.e)
		return t
	def decrypt(self,u,v): #decryption of message
		f1=modular_mult(u,self.__s)
		f2=modular_sub(v,f1)
		return f2    #decrypted message
class Bob:
	__m=None #message to be encrypted
	def __init__(self, r,e1,e2,m):
		self.r = r
		self.e1=e1
		self.e2=e2
		self.__m=m 
	def encrypt(self,A,t): #encryption if message m
		u=modular_mult(self.r,A)
		u=modular_add(u,self.e1)
		v=modular_mult(self.r,t)
		v=modular_add(v,self.e2)
		v=modular_add(v,self.__m)
		return u,v;        # cipher text
A=np.array([[1,2,4,11],
	[3,17,2,25],
	[2,7,3,14],
	[10,6,12,5]])
s=np.array([[1],[22],[6],[9]])
e=np.array([[0],[-1],[-1],[1]])
r=np.array([[0,5,2,12]])
e1=np.array([1,7,3,5])
e2=np.array([7])
m=np.array([6])%1
a=Alice(A,s,e) #making an object for Alice
b=Bob(r,e1,e2,m) #making an object for Bob
t=a.keyGen() 
u,v=b.encrypt(a.A, t) 
f2=a.decrypt(u,v)
#Testing the decrypted message
if f2[0]>(q/2): #testing
	f2[0]=1 
else:
	f2[0]=0
if f2[0]==m[0]:
	print("The message is decrypted correctly")
else:
	print("The message is decrypted incorrectly")
