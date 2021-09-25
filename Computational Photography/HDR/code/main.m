%
% convert an image set into HDR, then tone mapping it.
%
% input:
%   folder: the (relative) path containing the image set.
%   lambda: smoothness factor for gsolve.
%   [srow scol]: the dimension of the resized image for sampling in gsolve.
%
function main(folder, alpha_, white_, lambda, prefix, srow, scol)

    %%
    % handling default parameters
    if( ~exist('folder') )
        folder = '..\data\door_stack'; % no tailing slash!
    end
    if( ~exist('lambda') )
	      lambda = 1;
    end
    
    pkg load image
    
    disp('Read images with different exposures.');
    [simages, exposures] = readImages(folder);
    
    disp('Select 50 random pixels from each image.');
    width = size(simages{1},2);
    height = size(simages{1},1);
    numPixels = 50;
    numPics = length(simages);
    for i =1:numPixels
      w = width*0.3;
      h = height*0.3;
      x(i) = randi(w);
      y(i) = randi(h);
    endfor
    for j=1:numPics;
        image = simages{j};
        img = imresize(image,0.3);
        for i=1:numPixels;
            Zr(i,j) = img(y(i),x(i),1);
            Zg(i,j) = img(y(i),x(i),2);
            Zb(i,j) = img(y(i),x(i),3);
        end
    end
    
    ln_t = log(exposures);

    
    disp('Calculate camera response function by gsolve.');
    gcell = cell(3,1);
    number = size(simages,3);
    w = weightingFunction();
    
    [g{1},~] = gsolve(Zr, ln_t, lambda, w);
    [g{2},~] = gsolve(Zg, ln_t, lambda, w);
    [g{3},~] = gsolve(Zb, ln_t, lambda, w);
    
    t = cputime
    disp('Generate HDR');
  	imgHDR = HDRMap(simages, g, ln_t, w);
    t = cputime -t
    
    lightness = [ 0.06, 0.08, 0.1, 0.12,0.14]; 
    for num = 1 : size(lightness,2);
      mapImg = zeros(height, width, 3);
      for c = 1:3;
        hdrI = imgHDR(:,:,c);
        mapImg(:,:,c) = toneMapping(hdrI,lightness(num));
      end
      max(max(mapImg));
      min(min(mapImg));
      mapImg = round(mapImg*256);
      mapImg = uint8(mapImg);
      figure;
      imshow(mapImg)
      output_name = [ 'imgHDR_' num2str(lightness(num)) '.bmp' ];
      imwrite(mapImg, output_name);
    end


    disp('done!');
    
end
