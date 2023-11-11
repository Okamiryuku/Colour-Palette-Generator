import numpy as np
from PIL import Image
from flask import Flask, render_template

# Load the image using PIL
file_name = 'sample_img.jpeg'
image = Image.open(file_name)

# Convert the image to a NumPy array
image_array = np.array(image)

# Get the dimensions of the array
height, width, channels = image_array.shape

# Create a set to store unique pixel values
unique_values = set()

# Create a dictionary to store pixel value counts
pixel_counts = {}

# Iterate over the array to count pixel occurrences
for i in range(height):
    for j in range(width):
        pixel_value = tuple(image_array[i, j])
        pixel_counts[pixel_value] = pixel_counts.get(pixel_value, 0) + 1

# Get the top 10 repeated values
top_10_values = sorted(pixel_counts.items(), key=lambda x: x[1], reverse=True)[:12]

# Display or save the top 10 values
for value, count in top_10_values:
    print(f'Pixel Value: {value}, Count: {count}')

# Creating my Flask APP
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
