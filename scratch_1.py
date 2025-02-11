import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the image
img = Image.open('your_image_path.jpg.JPG').convert('L')
img_array = np.array(img)

# Compute the 2D Fourier transform
f = np.fft.fft2(img_array)
fshift = np.fft.fftshift(f)

# Plot the magnitude spectrum
magnitude_spectrum = 20 * np.log(np.abs(fshift))
plt.subplot(121), plt.imshow(img_array, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(magnitude_spectrum, cmap='gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()

# Alter the frequency by removing low-frequency components
rows, cols = img_array.shape
crow, ccol = int(rows / 2), int(cols / 2)  # Ensure crow and ccol are integers
fshift[int(crow - 30):int(crow + 30), int(ccol - 30):int(ccol + 30)] = 0

# Compute the inverse Fourier transform
f_ishift = np.fft.ifftshift(fshift)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

# Plot the original image and the altered image
plt.subplot(131), plt.imshow(img_array, cmap='gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132), plt.imshow(img_back, cmap='gray')
plt.title('Image after removing low freq'), plt.xticks([]), plt.yticks([])
plt.show()
