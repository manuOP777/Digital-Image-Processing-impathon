function main()
    % Load image
    image = imread('your_image_path.jpg'); % Provide the correct path to your image file here

    % Check if the image was loaded successfully
    if isempty(image)
        disp('Error: Unable to load image.');
        return;
    end

    % Set initial low and high thresholds
    low_threshold = 20;
    high_threshold = 20;

    % Display original image
    figure;
    imshow(image);
    title('Original Image');

    % Display filtered image
    figure;
    while true
        % Remove frequency components
        filtered_image = remove_frequency(image, low_threshold, high_threshold);

        % Display filtered image
        imshow(uint8(filtered_image));
        title('Filtered Image');

        % Wait for key press
        key = waitforbuttonpress;
        if key == 1  % Check if key press
            key = double(get(gcf,'CurrentCharacter'));
            if key == 113 % 'q' key
                break;
            elseif key == 97 % 'a' key
                low_threshold = low_threshold - 1;
            elseif key == 115 % 's' key
                low_threshold = low_threshold + 1;
            elseif key == 122 % 'z' key
                high_threshold = high_threshold - 1;
            elseif key == 120 % 'x' key
                high_threshold = high_threshold + 1;
            end

            % Reset thresholds if they exceed image dimensions
            [rows, cols, ~] = size(image);
            if low_threshold < 0
                low_threshold = 0;
            end
            if high_threshold < 0
                high_threshold = 0;
            end
            if low_threshold > min(rows, cols) / 2
                low_threshold = min(rows, cols) / 2;
            end
            if high_threshold > min(rows, cols) / 2
                high_threshold = min(rows, cols) / 2;
            end
        end
    end
    close all;
end

function filtered_image = remove_frequency(image, low_threshold, high_threshold)
    % Convert image to grayscale
    gray_image = rgb2gray(image);

    % Apply Fourier Transform
    f_transform = fft2(double(gray_image));
    f_transform_shifted = fftshift(f_transform);

    % Get image size
    [rows, cols] = size(gray_image);
    center_row = rows / 2;
    center_col = cols / 2;

    % Create mask to eliminate low and high frequency components
    mask = ones(rows, cols);
    mask(center_row - low_threshold:center_row + low_threshold, ...
         center_col - low_threshold:center_col + low_threshold) = 0;
    mask(center_row - high_threshold:center_row + high_threshold, ...
         center_col - high_threshold:center_col + high_threshold) = 0;

    % Apply mask
    f_transform_shifted_filtered = f_transform_shifted .* mask;

    % Apply Inverse Fourier Transform
    f_transform_filtered = ifftshift(f_transform_shifted_filtered);
    image_filtered = ifft2(f_transform_filtered);
    filtered_image = abs(image_filtered);
end

