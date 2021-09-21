%
% convert an image set into HDR, then tone mapping it.
%
% input:
%   folder: the (relative) path containing the image set.
%   lambda: smoothness factor for gsolve.
%   [srow scol]: the dimension of the resized image for sampling in gsolve.
%   prefix: output LDR's prefix
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
    if( ~exist('alpha_') )
	      alpha_ = 0.18;
    end
    if( ~exist('white_') )
	      white_ = 3;
    end
    if( ~exist('prefix') )
	      tokens = strsplit('/', folder);
	      prefix = char(tokens(end));
    end
    
    pkg load image
    
    disp('Read images with different exposures.');
    [simages, exposures] = readImages(folder);
    
    disp('Select 50 random pixels from each image.');
    width = size(simages{1},2);
    height = size(simages{1},1);
    numPixels = 50;
    numPics = length(simages);
    for i=1:numPixels;
        x = randi(width*0.3);
        y = randi(height*0.3);
        for j=1:numPics;
            img = imresize(simages{j},0.3);
            Zr(i,j) = img(y,x,1);
            Zg(i,j) = img(y,x,2);
            Zb(i,j) = img(y,x,3);
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
    %imgHDR = hdrDebevec(simages, g, ln_t, w);
    height = size(simages{1},1);
    width = size(simages{1},2);   
    hdrImg = zeros(height,width,3);
    for c = 1:3;
        for i = 1:height;
            for j = 1:width;
                wij = 0;
                lEg = 0;
                for k = 1:numPics;
                    lE = g{c}(simages{k}(i,j,c)+1) - ln_t(k);
                    lEg = w(simages{k}(i,j,c)+1)*lE + lEg;
                    wij = wij + w(simages{k}(i,j,c)+1); 
                end
                lEg = lEg/wij;
                hdrImg(i,j,c) = exp(lEg);
                hdrImg3(i,j,c) = lEg;
                %disp(j);
            end
            disp(i);
        end
    end

    %% for histogram picture
    hdrImgG = hdrImg3(:,:,2);
    imshow(hdrImgG);
    imgHDR = hdrImg;
    save('imgHDR.mat','imgHDR');
    t = cputime -t

    write_rgbe(imgHDR, [prefix '.hdr']);
    disp('constructing HDR radiance map.');
    
    %load('imgHDR.mat');
    imgTMO = tmoReinhard02(imgHDR, 'global', alpha_, 1e-6, white_);
    save('imgTMO.mat', 'imgTMO');
    disp('saving Final Tone mapped image');
    write_rgbe(imgTMO, [prefix '_tone_mapped.hdr']);
    imwrite(imgTMO, [prefix '_tone_mapped.png']);

    disp('done!');
    
end
