import cv2
import math
import numpy as np

#Non local means filter on an image
def nonlocalmeans(imgpath):
	img=cv2.imread(imgpath,cv2.IMREAD_GRAYSCALE)
	(M,N)= img.shape
	I=np.zeros((M,N),dtype=np.uint8)
	for i in range(M):
		for j in range(N):
			#Leaving the edge pixels
			if(i>2+2 and j>2+2 and i<M-3-2 and j<N-3-2):
				#Set a 7x7 patch as target patch
				TargetPatch=np.array(img[i-3:i+4,j-3:j+4])
				#Denoise patch will be the weighted Patch average
				DenoisePatch=np.zeros((7,7))
				SumofWeights=0
				#Calculate the weigths of surrounding patches
				for k in range(5):
					for l in range(5):
						SearchPatch=np.array(img[i+k-3-2:i+k+4-2,j+l-3-2:j+l+4-2])
						#Compute weight for a search patch w.r.t Target Patch
						W=computeWeight(TargetPatch,SearchPatch)

						#Multipying the weigt to each pixel in search patch 
						WeightedPatch=np.array([(x*W) for x in SearchPatch])
						
						DenoisePatch=DenoisePatch+WeightedPatch
						SumofWeights=SumofWeights+W
				#Normalization
				DenoisePatch=[(x/SumofWeights) for x in DenoisePatch]
				I[i-3:i+4,j-3:j+4]=DenoisePatch
	return I

#Weight of SPatch w.r.t TPatch
def computeWeight(TPatch,SPatch):
	(M,N)=TPatch.shape
	MSE=0
	var=100
	#print M,N
	for i in range(M):
		for j in range(N):
			MSE=MSE+((int(TPatch[i,j])-int(SPatch[i,j]))*int((TPatch[i,j])-int(SPatch[i,j])))
	W= math.exp(-((MSE)/(2*var*var)))

	return W

def Gaussianfilter(Tpatch):
	(M,N)=Tpatch.shape
	normalization=0;

	for i in range(M):
		for j in range(N):
			gaussian=gaussian2D([i,j],[3,3],10)
			Tpatch[i,j]=Tpatch[i,j]*gaussian
			normalization=normalization+gaussian

	Tpatch=np.array([x/normalization for x in Tpatch])
	return Tpatch


def gaussian2D(x,y,var):
	#return (1/(2*3.14)*var*var)*math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))
	return math.exp(-(((x[0]-y[0])*(x[0]-y[0]))+((x[1]-y[1])*(x[1]-y[1])))/(2*var*var))




C=nonlocalmeans("./lenna.noise.jpg")
#Dislapy the non -local means filter
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image',C)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('nonlocalmeans.png',C)
