import base64

# Function to convert a PNG file to base64 data
def png_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode('utf-8')

# Function to convert base64 data back to a PNG file
def base64_to_png(encoded_string, output_file_path):
    with open(output_file_path, "wb") as image_file:
        image_file.write(base64.b64decode(encoded_string))

# Example usage:
input_png = "input.png"
output_png = "output.png"

# Convert a PNG file to base64
base64_data = png_to_base64(input_png)

# Convert the base64 data back to a PNG file
base64_to_png(base64_data, output_png)
