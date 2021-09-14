%Reading Image and initialising variables
A=imread('lenna.noise.jpg');
[m,n]=size(A);
C=zeros(m+2,n+2);
B=padarray(A,[1 1]);    %Zero padding the image for Gradients
B=im2double(B);
lambda=0.15;
P=zeros(m+2,n+2,2);

%Original Image
figure;
subplot(2,4,1),imshow(B);
title('i = 0');

%Iterating using the anisotropic filter
z=7;
while(z)
for i=2:m+1
    for j=2:n+1
        Ix=B(i,j+1)-B(i,j);
        Iy=B(i-1,j)-B(i,j);
        delta=sqrt(Ix*Ix+Iy*Iy);
        c=1/(1+delta*delta/4);  %Computing c
        P(i,j,1)=c*Ix;          %Computing phi
        P(i,j,2)=c*Iy;
    end
end

for i=2:m+1
    for j=2:n+1
        C(i,j)=B(i,j)+lambda*(P(i,j,1)+P(i,j,2)-P(i+1,j,2)-P(i,j-1,1)); %Final pixel value in this iteration
    end
end
B=C;
subplot(2,4,9-z),imshow(B); %Plotting image of this iteration
str=sprintf('i = %d',8-z);
title(str);
z=z-1;
end