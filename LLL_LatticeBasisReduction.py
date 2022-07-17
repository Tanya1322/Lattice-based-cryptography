# This is an implementation for LLL lattice basis reduction problem in python. The LLL agorithm is used to break encryption by reducing the bad basis into good basis.
import numpy as np
import math
def magnitude(k):
	magnitude_k=0
	for i in range(len(B)):
		magnitude_k+=B[k][i]**2
	magnitude_k=math.sqrt(magnitude_k)
	return magnitude_k
def mul(a,b):
	temporary=[0]*len(b)
	for i in range(len(b)):
		temporary[i]=b[i]*a
	return temporary
def coeff(k,j):
	res=(magnitude(k)*magnitude(j))/(magnitude(j)*magnitude(j))
	return res
def SizeCondition(k,j):
	if coeff(k,j)<=0.5:
		return True
	else:
		return False
def UpdateGramSchmit(B):
	Borth[0]=B[0]
	for i in range(1,len(B)):
		temp=[]
		for j in range(i-1,-1,-1):
			temp3=coeff(i,j)
			temp.append(mul(temp3,Borth[j]))
		res=[0]*len(B)
		for j in range(len(temp)):
			res=np.add(res,temp[j])
		Borth[i]=B[i]-res
def LovaszCond(k):
	t=3/4-(coeff(k,k-1)**2)
	if magnitude(k)**2>=t*(magnitude(k-1)**2):
		return True
	else:
		return False
B=[]
n=int(input("Enter the no. of basis vectors"))
for i in range(n):
	lst=[]
	print("Enter coordinates for "+str(i+1)+" vector:")
	for j in range(n):
		lst.append(int(input()))
	B.append(lst)
Borth=[[0 for i in range(n)] for j in range(n)]
Borth[0]=B[0]
k=1
while k<len(B):
	for j in range(k-1,-1,-1):
		if not SizeCondition(k,j):
			B[k]=np.subtract(B[k],mul(int(coeff(k,j)),B[j]))
			UpdateGramSchmit(B)
	if LovaszCond(k):
		k=k+1
	else:
		B[k],B[k-1]=B[k-1],B[k]
		UpdateGramSchmit(B)
		k=max(k-1,1)
print("The reduced nearly orthogonal (good basis) are: ")
for i in range(n):
	print(B[i])
