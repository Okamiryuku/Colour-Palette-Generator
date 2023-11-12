import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for

# Creating my Flask APP
app = Flask(__name__)


def image_colour(file_path):
    image = Image.open(file_path)
    image_array = np.array(image)
    height, width, channels = image_array.shape
    black_threshold = 60
    white_threshold = 190

    pixel_counts = {}

    for i in range(height):
        for j in range(width):
            pixel_value = tuple(image_array[i, j])
            if all(value > black_threshold and value < white_threshold for value in pixel_value):
                # Update the count in the dictionary
                pixel_counts[pixel_value] = pixel_counts.get(pixel_value, 0) + 1

    sorted_values = sorted(pixel_counts.items(), key=lambda x: x[1], reverse=True)[:400]

    top_10_values = list(sorted_values[::20])

    return top_10_values


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser should show an error
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to the 'uploads' folder
            file_path = f"static/uploads/{file.filename}"
            file.save(file_path)

            # Process the image
            top_10_values = image_colour(file_path)

            # Render the result template with the top 10 values
            return render_template('result.html', image_path=file_path, top_10_values=top_10_values)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
