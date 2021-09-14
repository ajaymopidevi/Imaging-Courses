import cv2
import math
import numpy as np
def harriscorner(imgpath):
	img=cv2.imread(imgpath,cv2.IMREAD_GRAYSCALE)
	(M,N)= img.shape
	I=np.zeros((M,N),dtype=np.uint8)
	H=np.zeros((M,N),dtype=np.uint8)
	G=gaussianfilter(img,1)
	np.savetxt("Gaussian.csv",G, delimiter=",")
	for i in range(M):
		for j in range(N):
			if(i>1 and j>1 and i<M-1 and j<N-1):
				C=np.zeros((2,2),dtype=np.int)
				for k in range(3):
					for l in range(3):
						Ix= int(G[i+k-1,j])-int(G[i+k-2,j])
						Iy= int(G[i,j+l-1])-int(G[i,j+l-2])
						C[0,0]=C[0,0]+(Ix*Ix)
						C[0,1]=C[0,1]+(Ix*Iy)
						C[1,0]=C[1,0]+(Iy*Ix)
						C[1,1]=C[1,1]+(Iy*Iy)
				
				#Gxx=abs(int(G[i+1,j])+int(G[i-1,j])-2*int(G[i,j]))
				#Gxy=abs(int(G[i,j+1])-int(G[i,j])-int(G[i-1,j])+int(G[i-1,j+1]))
				#Gyx=abs(int(G[i,j])-int(G[i+1,j])-int(G[i,j-1])+int(G[i+1,j-1]))
				#Gyy=abs(int(G[i,j+1])+int(G[i,j-1])-2*int(G[i,j]))
				
				#C[0,0]=Gxx
				#C[0,1]=Gxy
				#C[1,0]=Gyx
				#C[1,1]=Gyy
				R=(C[1,1]*C[0,0])-(C[0,1]*C[1,0])-0.05*((C[0,0]+C[1,1])*(C[0,0]+C[1,1]))
			#	print R, C,(C[1,1]*C[0,0])-(C[0,1]*C[1,0])
				if(R>100000):
					I[i,j]=255
				else:
					I[i,j]= 0
	for i in range(M):
		for j in range(N):
			if(i>0 and j>0 and i<M-1 and j<N-1):
				if(I[i,j]==255):
					sum= 0
					for k in range(3):
						for l in range(3):
							sum=sum+I[i+k-1,j+l-1]
					if sum == 255:
						I[i,j]=255
					else:
						I[i,j]=0
	
	return I


def gaussianfilter(Img,var):
	(M,N)=Img.shape
	I=np.zeros((M,N),dtype=np.uint8)
	for i in range(M):
		for j in range(N):
			if(i>1 and j>1 and i<M-2 and j<N-2):
				I_u=int(Img[i,j])
				u=[i,j]
				normalization=0
				for k in range(5):
					for l in range(5):
						p=[k+i-2,l+j-2]
						#print p[0]-u[0], p[1]-u[1]
						I_p=int(Img[p[0],p[1]])
						W=gaussian2D(p,u,var)
						I[i,j]=I[i,j]+(I_p*W)
						normalization=normalization+(W)
				#print normalization
				I[i,j]=(I[i,j]/normalization)
			else:
				I[i,j]=Img[i,j]
	return I


def gaussian2D(x,y,var):
	return (1/(2*3.14)*var*var)*math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))
	#return math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))

C=harriscorner("./IITG.jpg")
img=cv2.imread("./IITG.jpg",cv2.IMREAD_GRAYSCALE)
(M,N)=img.shape
for i in range(M):
	for j in range(N):
		if (C[i,j]==255):
			cv2.circle(img,(j,i),10,25)			
			
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image',img)
cv2.namedWindow('Image1', cv2.WINDOW_NORMAL)
cv2.imshow('Image1',C)

cv2.waitKey(0)
cv2.destroyAllWindows()
#print C
np.savetxt("corner1.csv",C, delimiter=",")