import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps

# Configure the Streamlit page at the very beginning
st.set_page_config(page_title="Number Guesser", page_icon="🔢")


# --- Model Loading ---
# Using st.cache_resource to load the model only once, improving performance
@st.cache_resource
def load_robot():
    """Loads the pre-trained Keras model."""
    try:
        # Load your trained model. Replace "mnist_model.h5" with your model file if it's different.
        model = tf.keras.models.load_model("mnist_model.h5")
        return model
    except Exception as e:
        st.error(f"Error loading the model: {e}")
        st.stop()  # Stop the app if the model can't be loaded


robot = load_robot()

# --- App UI ---
st.title("🔢 Magic Number Guesser")
st.write("Upload a picture of a single digit (0-9) and I'll guess it!")

# Picture uploader component
uploaded_pic = st.file_uploader("Choose a number picture:", type=["png", "jpg", "jpeg"])

img = None  # Initialize img outside the if block

if uploaded_pic:
    # Prepare the picture: convert to grayscale and resize to 28x28 pixels
    try:
        img = Image.open(uploaded_pic).convert("L")  # Convert to grayscale (L mode)
        img = img.resize((28, 28))  # Resize to MNIST standard size

        # Check if we need to invert colors
        # MNIST dataset typically has white digits on a black background.
        # If the uploaded image is mostly light (e.g., black digit on white background),
        # we invert it to match the training data's style.
        if (
            np.mean(np.array(img)) > 128
        ):  # If the average pixel value is bright (mostly white)
            img = ImageOps.invert(img)  # Invert colors

        st.image(img, caption="Processed Image", width=150)

    except Exception as e:
        st.error(f"Error processing image: {e}")
        img = None  # Reset img to prevent further errors

# --- Prediction Button and Logic ---
# Only show the predict button if an image has been successfully uploaded and processed
if img is not None:
    if st.button("Predict"):
        # Display a spinner while the robot is thinking
        with st.spinner("Thinking..."):
            # Preprocess the image array for model prediction
            # Normalize pixel values to 0-1 (as typically done for neural networks)
            img_array = np.array(img) / 255.0

            # Add batch and channel dimensions
            # Keras models expect input in the shape (batch_size, height, width, channels)
            # For a single grayscale image (28x28), this becomes (1, 28, 28, 1)
            img_array = np.expand_dims(img_array, axis=(0, -1))

            # Make the prediction using the loaded model
            guess = robot.predict(img_array)

            # Get the predicted number (the index with the highest probability)
            number = np.argmax(guess)

            # Calculate the confidence of the prediction
            confidence = np.max(guess) * 100

        # Show the prediction results
        st.success(f"Predicted Digit: {number}")
        st.info(f"Confidence: {confidence:.1f}%")

        # Display confidence for each possible number (0-9) using progress bars
        st.write("Confidence for each number:")
        for i in range(10):
            st.progress(int(guess[0][i] * 100), text=f"{i}: {guess[0][i]*100:.1f}%")
else:
    st.info("Upload an image above to get a prediction.")

# --- Tips for Drawing ---
# Use an expander to keep the tips section collapsible and neat
with st.expander("💡 Tips for best results"):
    st.write(
        """
    For the best accuracy from the model, try to:
    - Draw numbers that are **centered** in the image.
    - Use **thick lines** for the digits.
    - Ensure your digits are **white** on a **dark background** (this matches the MNIST dataset's style).
    - Avoid drawing multiple digits or complex backgrounds.
    """
    )
    # Display an example image from Wikipedia to illustrate good drawing practices
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/2/27/MnistExamples.png",
        caption="Examples of good MNIST-style digits",
        width=300,
    )
