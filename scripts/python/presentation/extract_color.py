from PIL import Image
from matplotlib import pyplot as plt



# Load the image from file

image_path = 'color.jpg'

image = Image.open(image_path)
plt.imshow(image)


# Use the getcolors method to extract the colors from the image

# Since the image is small and we expect a few colors, we can assume all colors will be captured

colors = image.getcolors(maxcolors=1000)



# Extract the color values (assuming the colors are not repeated and are in the correct order)

color_values = [color[1] for color in colors]



color_values