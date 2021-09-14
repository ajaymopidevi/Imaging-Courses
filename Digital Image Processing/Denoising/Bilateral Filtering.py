import cv2
import math
import numpy as np
def bilateralfilter(imgpath,R_var,D_var):
	img=cv2.imread(imgpath,cv2.IMREAD_GRAYSCALE)
	(M,N)= img.shape
	I=np.zeros((M,N),dtype=np.uint8)
	for i in range(M):
		for j in range(N):
			try:

				if(i>2 and j>2 and i<M-3 and j<N-3):
					
					I_u=int(img[i,j])
					u=[i,j]
					normalization=0
					for k in range(5):
						for l in range(5):
							p=[k+i-1,l+j-1]
							#print p[0]-u[0], p[1]-u[1]
							I_p=int(img[p[0],p[1]])
							Wr=gaussian1D(I_p,I_u,R_var)
							#Wd=1
							Wd=gaussian2D(p,u,D_var)
							I[i,j]=I[i,j]+(I_p*Wr*Wd)
							normalization=normalization+(Wr*Wd)
					#print normalization
					I[i,j]=(I[i,j]/normalization)

				else:
					I[i,j]=img[i,j]
			except(ValueError):
				print normalization,Wr,Wd
				
	return I
def gaussian1D(x,y,var):
	#return (1/math.sqrt(2*3.14)*var)*math.exp(-((x-y)*(x-y))/(2*var*var))
	return math.exp(-((x-y)*(x-y))/(2*var*var))


def gaussian2D(x,y,var):
	#return (1/math.sqrt(2*3.14)*var)*math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))
	return math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))


I=bilateralfilter("./spunifnoisy.jpg",10,1)
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image',I)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('bilateralunif.png',I)
