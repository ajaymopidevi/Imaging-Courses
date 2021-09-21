function [images, exposureTimes] = readImages(folder, extension)
    
    if( ~exist('extension') )
	      extension = 'jpg';
    end

    files = dir([folder, '/*.', extension]);

    filename = [folder, '/', files(1).name];
    number = length(files);
    images = cell(number,1);
    exposureTimes = zeros(number, 1);

    for i = 1:number
        filename = [folder, '/', files(i).name];
        images{i} = imread(filename);
        info = imfinfo(filename);
      	exposureTimes(i) = info.DigitalCamera.ExposureTime;
    end
end
