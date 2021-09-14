import cv2
import numpy as np
import matplotlib.pyplot as plt


#Compute the Normalized histogram(cdf) of image of 'bins' bins
def computehist(img,bins):
	
	(M,N)= img.shape
	normalhist=np.zeros(bins)
	#Compute the histogram
	for i in range(M):
		for j in range(N):
			bin=img[i,j]/(256/bins);
			normalhist[bin]=normalhist[bin]+1
	

	p_normalhist=np.zeros(bins,dtype=np.int)
	sum=0
	#cdf of the histogram
	for i in range(bins):
		#Normalizing the histogram to find pdf
		normalhist[i]=normalhist[i]/(M*N)

		sum=sum+normalhist[i]
		#cdf at any point is sum of all pdf's till there i.e cdf(n-1)+pdf(n)
		p_normalhist[i]=(bins-1)*sum
	return p_normalhist


#Histogram Specification
def computez(hist,targethist):
	z=np.zeros(hist.size,dtype=np.int)
	for i in range((hist.size)):
		diff1=0
		diff2=0
		j=hist.size-1
		#calculating close value of target histogram to specific value in given image 
		while(diff1>=diff2):
			if(j>0):
				diff1=abs(hist[hist.size-i-1]-targethist[j])
				diff2=abs(hist[hist.size-i-1]-targethist[j-1])
				j=j-1

			else:
				j=1
				break
		z[hist.size-i-1]=j+1
	return z

givenimg=cv2.imread("./givenhist.jpg",cv2.IMREAD_GRAYSCALE)
#Calculate equalized histogram of given image of 256 bins
hist=computehist(givenimg,256)

spimg=cv2.imread("./sphist.jpg",cv2.IMREAD_GRAYSCALE)
#Calculate equalized histogram of target image of 256 bins
targethist=computehist(spimg,256)


#Histogram Specification
z=computez(hist,targethist)

modifiedimg=givenimg
for i in range(givenimg.shape[0]):
	for j in range(givenimg.shape[1]):
		s=givenimg[i,j]
		modifiedimg[i,j]=z[s]
modifiedhist=computehist(modifiedimg,256)


#Display the modified image
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image',modifiedimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('nolmeans.png',modifiedimg)
