function weight = weightingFunction()
    weight = zeros(256, 1);

    weight = [1:1:256];
    weight = min(weight, 256-weight);

end
