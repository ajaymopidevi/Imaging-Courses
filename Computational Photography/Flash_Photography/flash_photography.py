import numpy as np
import cv2

def range_kernel(patch, sigma=1.5):
	patch_shape = patch.shape
	size =patch_shape[0]*patch_shape[1]
	patch = np.reshape(patch, (size))
	center = size//2
	I = patch[center]
	kernel = [np.exp(-0.5*np.square(patch[x]-I)/np.square(sigma)) for x in range(size)]
	kernel = np.array(kernel)
	kernel = kernel/np.sum(kernel)
	kernel = np.reshape(kernel,patch_shape)


	return kernel

def domain_kernel(l=3, sig=1.):
	ax = np.linspace(-(l-1)/2., (l-1)/2., l)
	xx, yy = np.meshgrid(ax, ax)

	kernel = np.exp(-0.5*(np.square(xx)+np.square(yy))/np.square(sig))

	return kernel/np.sum(kernel)

def bilateralFilter(img1, img2, dsig=28,rsig=30):
	img_shape = img1.shape
	kernel_size = 9
	k = kernel_size//2
	transform_img = np.zeros(img_shape)
	domain_filter = domain_kernel(kernel_size,dsig)
	p2d = ((k, k),
		   (k, k),
		   (0,0))
	img1 = np.pad(img1, p2d, 'symmetric')
	img_shape = img1.shape
	img2 = np.pad(img2, p2d, 'symmetric')

	for c in range(img_shape[2]):
		for i in range(k,img_shape[0]-k):
			for j in range(k, img_shape[1]-k):
				patch1 = img1[i-k:i+k+1, j-k:j+k+1, c]
				patch2 = img2[i-k:i+k+1, j-k:j+k+1, c]
				range_filter = range_kernel(patch2,rsig)
				kernel = np.multiply(range_filter, domain_filter)
				patch_blur = np.multiply(patch1, kernel)


				transform_img[i-k, j-k, c] = np.sum(patch_blur)/np.sum(kernel)



	return transform_img


flash_imgpath = r'./data/lamp/lamp_flash.tif'
ambient_imgpath = r'./data/lamp/lamp_ambient.tif'

flash_image = cv2.imread(flash_imgpath)
ambient_image = cv2.imread(ambient_imgpath)

F = np.array(flash_image, dtype=np.float)
A = np.array(ambient_image, dtype=np.float)

A_base = bilateralFilter(A, A)
cv2.imwrite('A_base.png',A_base)
A_NR = bilateralFilter(A, F)
cv2.imwrite('A_NR.png',A_NR)
F_base = bilateralFilter(F, F)
cv2.imwrite('F_base.png',F_base)
e = 0.02
F_detail = (F + e)/(F_base + e)
cv2.imwrite('F_detail.png',F_detail)

Flin = cv2.cvtColor(F, cv2.COLOR_BGR2GRAY)
Alin = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
M = (Flin - Alin )>10
cv2.imwrite('M.png',M*255)
mask = np.zeros(F.shape)
mask[:,:,0] = M
mask[:,:,1] = M
mask[:,:,2] = M

M = mask
A_final = ((1-M)* A_NR *F_detail) + (M*A_base)
cv2.imwrite('A_final.png',A_final)
print("Done")

