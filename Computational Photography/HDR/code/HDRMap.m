function imgHDR = HDRMap(simages, g, ln_t, w)    
    numPics = length(simages);
    height = size(simages{1},1);
    width = size(simages{1},2);   
    imgHDR = zeros(height,width,3);
    for c = 1:3;
        for i = 1:height;
            for j = 1:width;
                wij = 0;
                lEg = 0;
                for k = 1:numPics;
                    idx = simages{k}(i,j,c)+1;
                    lE = g{c}(idx) - ln_t(k);
                    lEg = w(idx)*lE + lEg;
                    wij = wij + w(idx); 
                end
                lEg = lEg/wij;
                imgHDR(i,j,c) = exp(lEg);
                imgHDR3(i,j,c) = lEg;
                
            end
        end
    end

    %% for histogram picture
    imgHDRG = imgHDR3(:,:,2);
    imshow(imgHDRG);
    
    minP = min(min(min(imgHDR)));
    for c=1:3
        imgHDR(:,:,c) = imgHDR(:,:,c)/minP;
    end
    
    %save('imgHDR.mat','imgHDR');
    
 end 