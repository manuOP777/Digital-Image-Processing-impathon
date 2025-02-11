import cv2
import numpy as np


def remove_frequency(image, low_threshold, high_threshold):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Fourier Transform
    f_transform = np.fft.fft2(gray_image)
    f_transform_shifted = np.fft.fftshift(f_transform)

    # Get image shape
    rows, cols = gray_image.shape
    center_row, center_col = rows // 2, cols // 2

    # Create mask to eliminate low and high frequency components
    mask = np.ones((rows, cols), np.uint8)
    mask[center_row - low_threshold:center_row + low_threshold,
    center_col - low_threshold:center_col + low_threshold] = 0
    mask[center_row - high_threshold:center_row + high_threshold,
    center_col - high_threshold:center_col + high_threshold] = 0

    # Apply mask
    f_transform_shifted_filtered = f_transform_shifted * mask

    # Apply Inverse Fourier Transform
    f_transform_filtered = np.fft.ifftshift(f_transform_shifted_filtered)
    image_filtered = np.fft.ifft2(f_transform_filtered)
    image_filtered = np.abs(image_filtered)

    return image_filtered


def main():
    # Load image
    image = cv2.imread('C:/Users/asus/Desktop/IMPATHON/your_image.jpg')


    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to load image.")
        return

    # Set initial low and high thresholds
    low_threshold = 20
    high_threshold = 20

    while True:
        # Remove frequency components
        filtered_image = remove_frequency(image, low_threshold, high_threshold)

        # Display image
        cv2.imshow('Filtered Image', filtered_image.astype(np.uint8))

        # Get key press
        key = cv2.waitKey(1) & 0xFF

        # Adjust thresholds based on key press
        if key == ord('q'):
            break
        elif key == ord('a'):
            low_threshold -= 1
        elif key == ord('s'):
            low_threshold += 1
        elif key == ord('z'):
            high_threshold -= 1
        elif key == ord('x'):
            high_threshold += 1

        # Reset thresholds if they exceed image dimensions
        rows, cols = image.shape[:2]
        if low_threshold < 0:
            low_threshold = 0
        if high_threshold < 0:
            high_threshold = 0
        if low_threshold > min(rows, cols) // 2:
            low_threshold = min(rows, cols) // 2
        if high_threshold > min(rows, cols) // 2:
            high_threshold = min(rows, cols) // 2

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
