# This is an implementation for LLL lattice basis reduction problem in python. The LLL agorithm is used to break encryption by reducing the bad basis into good basis.
import numpy as np
import math

def magnitude(k,b):
	magnitude_k=0
	for i in range(len(b)):
		magnitude_k+=b[k][i]**2
	magnitude_k=math.sqrt(magnitude_k)
	return magnitude_k

def dotProduct(a,b):
	res=0
	for i in range(n):
		res+=a[i]*b[i]
	return res

def coeff(k,j):
	res=dotProduct(B[k],Borth[j])/dotProduct(Borth[j],Borth[j])
	#print(res)
	return res

def mul(a,b):
	temporary=[0]*len(b)
	for i in range(len(b)):
		temporary[i]=b[i]*a
	return temporary

def SizeCondition(k,j):
	if coeff(k,j)<=0.5:
		print(True)
		return True
	else:
		print(False)
		return False

def LovaszCond(k):
	t=3/4-(coeff(k,k-1)**2)
	#print(t)
	if magnitude(k,Borth)**2>=t*(magnitude(k-1,Borth)**2):
		print("Lovasz cond: True")
		return True
	else:
		print("Lovasz Condition: False")
		return False

def UpdateGramSchmit(B):
	Borth[0]=B[0]
	for i in range(1,len(B)):
		temp=[]
		for j in range(i-1,-1,-1):
			temp3=coeff(i,j)
			#print(temp3)
			temp.append(mul(temp3,Borth[j]))
		res=[0]*len(B)
		for j in range(len(temp)):
			res=np.add(res,temp[j])
		Borth[i]=B[i]-res

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
UpdateGramSchmit(B)
print(Borth)
#print(Borth)
while k<len(B):
	for j in range(k-1,-1,-1):
		if not SizeCondition(k,j):
			B[k]=np.subtract(B[k],mul(round(coeff(k,j)),B[j]))
			print(B)
			UpdateGramSchmit(B)
			#print(B)
	if LovaszCond(k):
		k=k+1
	else:
		B[k],B[k-1]=B[k-1],B[k]
		print("After Swapping"+str(B))
		UpdateGramSchmit(B)
		print(Borth)
		#print(Borth)
		k=max(k-1,1)
print("The reduced nearly orthogonal (good basis) are: ")
for i in range(n):
	print(B[i])
