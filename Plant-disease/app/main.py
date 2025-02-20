import os
import json
from PIL import Image
import numpy as np
import tensorflow as tf
import streamlit as st
import base64

# Set page config to wide mode
st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌾",
    layout="wide"  # Set layout to wide
)

# Define the working directory and paths
working_dir = os.path.dirname(os.path.abspath(__file__))
model_path = f"{working_dir}/trained_model/plant_disease_prediction_model.h5"
class_indices_path = f"{working_dir}/class_indices.json"

# Load the pre-trained model
model = tf.keras.models.load_model(model_path)

# Load the class names
with open(class_indices_path) as f:
    class_indices = json.load(f)

# Function to load and preprocess the image using Pillow
def load_and_preprocess_image(image, target_size=(224, 224)):
    img = Image.open(image)
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype('float32') / 255.  # Normalize the image
    return img_array

# Function to predict the class of an image
def predict_image_class(model, image, class_indices):
    preprocessed_img = load_and_preprocess_image(image)
    predictions = model.predict(preprocessed_img)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    predicted_class_name = class_indices[str(predicted_class_index)]
    return predicted_class_name

# Function to set a full-screen background image
def add_background(image_path):
    with open(image_path, "rb") as image_file:
        img = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{img});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh;
            margin: 0;
            padding: 0;
        }}

        /* Sidebar background color and positioning */
        [data-testid="stSidebar"] {{
            background-color: #8B4513 !important; /* Brown background */
        }}

        /* Sidebar content styling */
        .stSidebar .css-1y4p8pa {{
            color: #FFFFFF;
            font-weight: bold;
        }}

        /* Main text styling */
        h1 {{
            color: #FFFFFF; 
            font-weight: 900; 
            font-size: 4em; 
            text-shadow: 3px 3px 6px #000000; 
        }}
        h2 {{
            color: #4B3D2A;  /* Dark brown text color */
            font-weight: 800; 
            font-size: 2.5em; 
            text-shadow: 2px 2px 5px #000000; 
        }}
        h3 {{
            color: #E76F51; 
            font-weight: 700; 
            font-size: 1.75em; 
            text-shadow: 2px 2px 4px #000000; 
        }}
        p, .small-text {{
            color: #FFFFFF; 
            font-size: medium; 
            font-weight: 600; 
            text-shadow: 1px 1px 3px #000000; 
        }}
        .white-text {{
            color: #FFFFFF; 
            font-weight: 700; 
            text-shadow: 1px 1px 3px #000000; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image using the provided path
add_background(r'C:\Users\saart\Downloads\finallimg.avif')  # Use raw string to avoid escape characters

# Disease treatment dictionary

treatment_suggestions = {
    "Apple___Apple_scab": {
        "Symptoms": "Dark, olive-colored spots on leaves and fruit. Leaves may become twisted or curled, and fruit may have scabs.",
        "Treatment": "Remove and destroy fallen leaves. Apply fungicides during early spring.",
        "Products": ["Bonide Captan Fungicide", "Southern Ag Mancozeb Flowable", "Garden Safe Fungicide3 (Copper)"]
    },
    "Apple___Black_rot": {
        "Symptoms": "Circular black lesions on fruit, leaves, and bark. Leaf spots appear brown or purple with black borders.",
        "Treatment": "Prune out and destroy infected branches. Apply copper-based fungicides.",
        "Products": ["Spectracide Immunox Multi-Purpose Fungicide", "Bonide Copper Fungicide", "Southern Ag Liquid Copper Fungicide"]
    },
    "Apple___Cedar_apple_rust": {
        "Symptoms": "Orange, gelatinous spores on leaves. Leaves develop yellow or orange spots.",
        "Treatment": "Remove nearby cedar trees. Apply fungicides like Myclobutanil or Mancozeb in early spring.",
        "Products": ["Immunox Fungicide", "Bonide Mancozeb Fungicide", "Safer Brand Garden Fungicide (Sulfur)"]
    },
    "Apple___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Maintain proper pruning, watering, and watch for early signs of disease.",
        "Products": ["Bonide Neem Oil", "Southern Ag Liquid Copper Fungicide"]
    },
    "Blueberry___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Prune bushes for air circulation, water properly, and apply preventive treatments during wet conditions.",
        "Products": ["Bonide Neem Oil", "Southern Ag Liquid Copper Fungicide"]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "Symptoms": "White powdery spots on leaves, stems, and fruit. Affected leaves may curl or become distorted.",
        "Treatment": "Prune affected areas to improve airflow. Apply sulfur or potassium bicarbonate-based fungicides.",
        "Products": ["Bonide Sulfur Plant Fungicide", "GreenCure Fungicide", "Safer Brand Garden Fungicide"]
    },
    "Cherry_(including_sour)___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Maintain proper care and monitor for disease early. Apply preventive sprays if needed.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "Symptoms": "Small, rectangular lesions on leaves that become grayish-brown with a yellow halo.",
        "Treatment": "Rotate crops and remove infected plant debris. Apply fungicides early.",
        "Products": ["Quadris Fungicide", "Heritage Fungicide"]
    },
    "Corn_(maize)___Common_rust_": {
        "Symptoms": "Small, raised pustules that are reddish-brown on leaves. These pustules break open to release spores.",
        "Treatment": "Remove plant debris after harvest. Apply fungicides such as Mancozeb or Azoxystrobin.",
        "Products": ["Dithane M-45 Fungicide", "Heritage Fungicide", "Quadris Fungicide"]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "Symptoms": "Lesions on leaves start as small spots, elongating into gray-brown streaks.",
        "Treatment": "Rotate crops and remove plant debris. Apply fungicides at early stages.",
        "Products": ["Quadris Fungicide", "Heritage Fungicide"]
    },
    "Corn_(maize)___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Regularly monitor for diseases and apply preventive care such as crop rotation.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
    "Grape___Black_rot": {
        "Symptoms": "Black lesions on leaves, stems, and fruit. Fruit shrivels into hard, black mummies.",
        "Treatment": "Remove and destroy infected leaves and fruit. Apply fungicides like Mancozeb and Captan in early spring.",
        "Products": ["Bonide Captan Fungicide", "Southern Ag Mancozeb Flowable Fungicide"]
    },
    "Grape___Esca_(Black_Measles)": {
        "Symptoms": "Brown or black spots appear on leaves, with eventual leaf necrosis. Fruit may develop dark streaks or black spots.",
        "Treatment": "Prune infected wood and ensure proper drainage. Apply preventive fungicides.",
        "Products": ["Bonide Copper Fungicide", "Southern Ag Mancozeb Fungicide"]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "Symptoms": "Brown, angular spots on leaves, leading to defoliation.",
        "Treatment": "Prune affected areas and apply fungicides like Mancozeb or Copper-based products.",
        "Products": ["Bonide Copper Fungicide", "Southern Ag Mancozeb Fungicide"]
    },
    "Grape___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Ensure proper pruning and care for healthy growth.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
    "Potato___Early_blight": {
        "Symptoms": "Dark, concentric rings on older leaves. Leaves may yellow and die.",
        "Treatment": "Rotate crops and apply fungicides like Chlorothalonil.",
        "Products": ["Daconil", "Ortho Garden Disease Control"]
    },
    "Potato___Late_blight": {
        "Symptoms": "Dark, greasy spots on leaves, which may turn grayish. Stems may rot.",
        "Treatment": "Remove infected plants immediately. Apply preventive fungicides.",
        "Products": ["Mefenoxam", "Ortho Garden Disease Control"]
    },
    "Potato___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Monitor for early signs of disease, and ensure proper care.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
    "Strawberry___Leaf_scorch": {
        "Symptoms": "Brown edges on leaves, leading to wilting.",
        "Treatment": "Avoid overhead watering and improve airflow around plants.",
        "Products": ["Fungicides with Trifloxystrobin", "Potassium Bicarbonate"]
    },
    "Strawberry___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Maintain good cultural practices, monitor for diseases.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
    "Tomato___Bacterial_spot": {
        "Symptoms": "Small, dark lesions on leaves. Leaves may drop, leading to wilting.",
        "Treatment": "Remove infected plants and avoid overhead watering.",
        "Products": ["Copper Fungicide", "Serenade Garden"]
    },
    "Tomato___Early_blight": {
        "Symptoms": "Dark, concentric spots on leaves, yellowing leaves, and stunted growth.",
        "Treatment": "Rotate crops and apply fungicides like Chlorothalonil.",
        "Products": ["Daconil", "Ortho Garden Disease Control"]
    },
    "Tomato___Late_blight": {
        "Symptoms": "Large, irregularly-shaped brown spots on leaves. Stems may rot.",
        "Treatment": "Remove infected plants and apply preventive fungicides.",
        "Products": ["Mefenoxam", "Ortho Garden Disease Control"]
    },
    "Tomato___healthy": {
        "Symptoms": "No disease symptoms; healthy plant.",
        "Treatment": "Monitor for early signs of disease, and ensure proper care.",
        "Products": ["Neem Oil", "Copper Fungicide"]
    },
}

  


# Main app function
def main():
    # Sidebar for navigation
    st.sidebar.title("DASHBOARD")
    st.sidebar.write("<hr>", unsafe_allow_html=True)
    selection = st.sidebar.radio("Go to:", ["Home", "Disease Detection", "Disease Treatment"])

    # Home section
    if selection == "Home":
        st.title('🌾 Welcome to Krishi Kaya: Disease Doctor 🌾')
        st.subheader('Empowering Farmers for a Healthier Crop Yield')
        st.write(""" 
        At **Krishi Kaya**, we are dedicated to empowering farmers with the tools and knowledge necessary to ensure their crops remain healthy and productive. Our platform leverages cutting-edge technology to help identify plant diseases quickly and accurately, allowing farmers to take timely action and minimize loss.
        """)

        st.subheader('Comprehensive Disease Detection')
        st.write(""" 
        Utilizing advanced machine learning algorithms, our **Disease Detection** feature allows users to upload images of their plants to receive immediate feedback on potential diseases. This service not only saves time but also provides essential insights into the health of crops, ensuring that farmers can respond effectively to any issues that arise.
        """)

        st.subheader('Tailored Treatment Suggestions')
        st.write(""" 
        Once a disease is identified, the **Disease Treatment** section offers personalized recommendations based on the specific plant disease detected. Our suggestions encompass a variety of remedies, including organic solutions, pesticides, and agricultural practices tailored to enhance plant health. This feature empowers farmers to choose the most effective and environmentally friendly options available.
        """)

        st.subheader('Get Started Today!')
        st.write(""" 
        Ready to enhance your farming experience? Explore our features now! Navigate to the **Disease Detection** section to upload a plant image, or check out the **Disease Treatment** section for effective remedies. Together, we can ensure the health of your crops and the prosperity of your farm!
        """)

    # Disease Detection section
    elif selection == "Disease Detection":
        st.title('🌿 Plant Disease Classifier 🌿')

        # File uploader for the image
        uploaded_image = st.file_uploader("Upload an image of a plant leaf", type=["jpg", "jpeg", "png"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((150, 150))
                st.image(resized_img, caption="Uploaded Image", use_column_width=False)

            with col2:
                if st.button('Classify'):
                    # Predict the disease using the model
                    prediction = predict_image_class(model, uploaded_image, class_indices)
                    st.success(f'Prediction: **{prediction}**', icon="✅")

                    # Show treatment suggestions for the predicted disease
                    if prediction in treatment_suggestions:
                     treatment = treatment_suggestions[prediction]
                    symptoms = treatment["Symptoms"]
                    treatment_info = treatment["Treatment"]
                    products = treatment["Products"]

                    st.write("### Treatment Suggestions:")
                    st.write(f"**Symptoms:** {symptoms}")
                    st.write(f"**Treatment:** {treatment_info}")
                    st.write(f"**Recommended Products:**")
                    for product in products:
                     st.markdown(f"<p style='color: white;'>{product}</p>", unsafe_allow_html=True)
                else:
                    st.write("No treatment suggestions available for this disease.")
                





    # Disease Treatment section
    elif selection == "Disease Treatment":
        st.title('🚜 Disease Treatment Suggestions 🚜')
        st.write("Based on common plant diseases, here are some treatment suggestions:")
        
        # Display all treatment suggestions
        for disease, treatment in treatment_suggestions.items():
            st.subheader(f"🌿 Disease: {disease}")
            st.write(f"<span class='white-text'>Treatment:</span> {treatment}", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
