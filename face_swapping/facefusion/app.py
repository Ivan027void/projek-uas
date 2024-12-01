import os
import sys
import streamlit as st
from PIL import Image
import io
import subprocess
import tempfile

# Placeholder for the face swapping function
# This function should take two images and return the swapped face image
def swap_faces(image1, image2):
    temp_dir = 'images'
    save_image_path = os.path.join(temp_dir, "save_image.png")

    # Get the Python interpreter from the virtual environment
    python_interpreter = sys.executable

    # Run the face fusion script using the subprocess module
    args = [python_interpreter, "facefusion.py", "--input", image1, "--source", image2, "--savepath", save_image_path]
    try:
        # Run the command and capture the output
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        print("Subprocess output:", result.stdout)
        print("Subprocess error (if any):", result.stderr)

        # Read the swapped image from the save path
        with open(save_image_path, "rb") as f:
            swapped_image_data = f.read()
            return Image.open(io.BytesIO(swapped_image_data))

    except subprocess.CalledProcessError as e:
        print("Subprocess failed with error:", e.stderr)
        return None  # Indicate error
    except Exception as e:
        print("An unexpected error occurred:", e)
        return None  # Indicate error

st.title("Face Swap App")

# File uploader for the first image
uploaded_file1 = st.file_uploader("Choose the target image to be swap", type=["jpg", "jpeg", "png"])

# File uploader for the second image
uploaded_file2 = st.file_uploader("Choose the soruce face image  ", type=["jpg", "jpeg", "png"])

if uploaded_file1 and uploaded_file2:
    # Display the uploaded images
    image1 = Image.open(uploaded_file1)
    image2 = Image.open(uploaded_file2)

    temp_dir = tempfile.mkdtemp()
    image1_path = os.path.join(temp_dir, uploaded_file1.name)
    image2_path = os.path.join(temp_dir, uploaded_file2.name)
    image1.save(image1_path)
    image2.save(image2_path)
    
    # st.image(image1, caption='First Image', use_column_width=True)
    # st.image(image2, caption='Second Image', use_column_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image1, caption='First Image', use_column_width=True)

    with col2:
        st.image(image2, caption='Second Image', use_column_width=True)
        
    if st.button('Swap Faces'):
        # Perform face swap
        swapped_image = swap_faces(image1_path, image2_path)
        
        # Display the result (if successful)
        if swapped_image:
            st.image(swapped_image, caption='Swapped Face Image', use_column_width=True)
        else:
            st.error("Error: Face swap failed.")
