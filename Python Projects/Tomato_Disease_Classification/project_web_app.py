# Importing the dependencies
import streamlit as st
import tensorflow as tf
import numpy as np
import os
from PIL import Image
import io

# Custom CSS to change background color
st.markdown(
    """
    <style>
    .main {
        background-color: #d8e4a1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Define the class names for the tomato diseases
class_names = [
    "bacterial spot", "early blight", "healthy tomato", "late blight",
    "southern blight"
]

@st.cache_data
def load_model():
    model_path = "Project_Improved_Model2.keras"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"The model file was not found at: {model_path}")
    model = tf.keras.models.load_model(model_path)
    return model

# Define the tomato disease solution function
def tomato_disease_solution(disease):
    solutions = {
        "bacterial spot": "Bacterial Spot Solution:\n"
                          "1. Use certified disease-free seeds.\n"
                          "2. Avoid overhead watering to reduce leaf wetness.\n"
                          "3. Apply copper-based bactericides as a preventative measure.\n"
                          "4. Remove and destroy infected plant debris.\n"
                          "5. Maintain proper plant spacing for air circulation.\n",
        "early blight": "Early Blight Solution:\n"
                        "1. Rotate crops to prevent pathogen buildup in the soil.\n"
                        "2. Use resistant tomato varieties.\n"
                        "3. Remove and destroy affected plant parts.\n"
                        "4. Apply fungicides like chlorothalonil or copper-based sprays.\n"
                        "5. Ensure proper plant spacing for good air circulation.\n",
        "healthy tomato": "Healthy Tomato Maintenance:\n"
                          "1. Ensure proper watering - water at the base, not overhead.\n"
                          "2. Use mulch to retain soil moisture and prevent soil-borne diseases.\n"
                          "3. Fertilize regularly with balanced nutrients.\n"
                          "4. Prune to promote good air circulation.\n"
                          "5. Monitor plants regularly for any signs of disease or pests.\n",
        "late blight": "Late Blight Solution:\n"
                       "1. Use resistant tomato varieties.\n"
                       "2. Remove and destroy infected plants immediately.\n"
                       "3. Apply fungicides containing mancozeb or chlorothalonil.\n"
                       "4. Avoid overhead watering to minimize moisture.\n"
                       "5. Practice crop rotation and soil sanitation.\n",
        "southern blight": "Southern Blight Solution:\n"
                           "1. Rotate crops to avoid soilborne pathogens.\n"
                           "2. Apply fungicides such as PCNB (pentachloronitrobenzene).\n"
                           "3. Remove and destroy infected plants and debris.\n"
                           "4. Use deep plowing to bury sclerotia.\n"
                           "5. Maintain proper soil drainage to prevent moisture buildup.\n"
    }
    return solutions.get(disease, "Unknown disease. Please provide a valid disease name.")

# Function to preprocess the image and predict the disease
def predict(model, img):
    # Preprocess the image
    img = img.resize((256, 256))  # Resize to match model input size
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image

    # Make predictions
    try:
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_index]
        confidence = round(100 * np.max(predictions[0]), 2)
        disease_solution = tomato_disease_solution(predicted_class)
        return predicted_class, confidence, disease_solution
    except Exception as e:
        st.error(f"Prediction failed: {e}")
        return None, None, None

# Load the model once and reuse it
model = load_model()

st.sidebar.image("Logo.jpg", use_column_width=True)
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "Prediction", "About", 'FAQ'])

if app_mode == "Home":
    # Custom styling for Home page
    st.markdown(
        """
        <style>
        .home-page {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        .home-header {
                color: #e41303;
                text-align: center;
                font-size: 32px;
                margin-bottom: 20px;
                font-weight: bold;
        }
        .section-header {
                color: #1e7910;
                font-size: 24px;
                margin-top: 20px;
                margin-bottom: 10px;
                font-weight: bold;
        }
        .section-content {
                color: #555555;
                font-size: 16px;
                margin-bottom: 15px;
        }
        .mission-statement {
            color: #2e8b57;
            text-align: justify;
            font-size: 18px;
        }
        .contact-details {
            background-color: #e0ebeb;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display logo with styling
    logo = Image.open("toma.jpg")
    st.image(logo, width=200, caption="Tomato Plant Disease Classification System", use_column_width=True)

    # Main header
    st.header("Welcome to the Tomato Plant Disease Classification System! 🍅🔍")

    # Introduction text
    st.write("""
    **Detect and Manage Tomato Plant Diseases** with ease using our cutting-edge machine learning technology. Our system helps you diagnose diseases from images of your tomato plants and provides actionable solutions to keep your plants healthy and thriving.
    """)

    # Get Started section with call-to-action
    st.markdown("### 🚀 Get Started")
    st.write("""
    1. **Upload an Image:** Navigate to the **Disease Recognition** page to upload an image of your tomato plant.
    2. **Receive Diagnosis:** Our system will analyze the image and provide a diagnosis along with actionable solutions.
    3. **Explore More:** Visit the **Home** page to learn more about our system and its capabilities.
    """)

    # Footer or additional information
    st.markdown("""
    **Need Assistance?** Navigate through the Dashboard and Visit our **[FAQ]** or **[About Us]** for support.
    """)

elif app_mode == "Prediction":
    st.subheader("Tomato Leaf Disease Detection 🌿🔍")
    st.write("""
    **Capture or Upload an Image of a Tomato Leaf** to diagnose the disease and receive actionable solutions.
    """)
    # Image capture/upload options
    col1, col2 = st.columns([1, 1])

    with col1:
        camera_file = st.camera_input("📸 Take a Picture")

    with col2:
        uploaded_file = st.file_uploader("🔄 Choose an Image", type=["jpg", "jpeg", "png"])

    img = None

    if camera_file is not None:
        img = Image.open(io.BytesIO(camera_file.getvalue()))
    elif uploaded_file is not None:
        img = Image.open(uploaded_file)

    if img:
        st.image(img, caption="Uploaded Image", use_column_width=True)

        # Perform prediction
        if st.button("Predict"):
            with st.spinner("Classifying..."):
                predicted_class, confidence, disease_solution = predict(model, img)

                if predicted_class:
                    st.success(f"Prediction: {predicted_class} ({confidence}% confidence)")
                    st.info(disease_solution)
    else:
        st.warning("Please upload an image or capture one using your camera.")

elif app_mode == "About":

        # Custom styling for About page
        st.markdown(
            """
            <style>
            .about-page {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }
            .about-header {
                color: #ff6347;
                text-align: center;
                font-size: 32px;
                margin-bottom: 20px;
                font-weight: bold;
            }
            .section-header {
                color: #2e8b57;
                font-size: 24px;
                margin-top: 20px;
                margin-bottom: 10px;
                font-weight: bold;
            }
            .section-content {
                color: #555555;
                font-size: 16px;
                margin-bottom: 15px;
            }
            .team-member {
                margin-top: 10px;
            }
            .team-member img {
                border-radius: 50%;
                width: 100px;
                height: 100px;
            }
            .team-member-name {
                font-weight: bold;
                color: #2e8b57;
            }
            .contact-info {
                background-color: #e0ebeb;
                padding: 15px;
                border-radius: 8px;
                margin-top: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # About Page Header
        st.markdown("<div class='about-page'><h1 class='about-header'>About the Tomato Plant Disease Classification System</h1></div>", unsafe_allow_html=True)

        # Mission Statement
        st.markdown("<div class='section-header'>Our Mission</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-content'>
            Our mission is to empower farmers, gardeners, and researchers with advanced technology to identify and manage diseases affecting tomato plants swiftly and accurately. By leveraging state-of-the-art machine learning algorithms, we aim to enhance plant health and increase crop yields, ensuring a sustainable future for agriculture.
            </div>
            """,
            unsafe_allow_html=True
        )

        # Goal
        st.markdown("<div class='section-header'>Our Goal</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-content'>
            The primary goal of our Tomato Plant Disease Classification System is to provide a reliable, user-friendly tool that can diagnose tomato plant diseases from images. We strive to offer actionable insights and effective solutions, helping users to take timely actions to protect their crops and improve overall plant health.
            </div>
            """,
            unsafe_allow_html=True
        )

        # Dataset
        st.markdown("<div class='section-header'>The Dataset</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-content'>
            Our system utilizes a comprehensive dataset of tomato plant images that include various disease categories. The dataset is curated from reliable sources and includes a diverse range of images to ensure accurate and robust disease detection. We continuously update and expand the dataset to improve the system's performance and adapt to new disease strains.
            </div>
            """,
            unsafe_allow_html=True
        )

        # The Team
        st.markdown("<div class='section-header'>Meet The Team</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-content'>
            <div class='Expert Team'>

            Our team behind the Tomato Plant Disease Classification System consists of experts in data science, machine learning, plant pathology, and experienced farmers. Together, we work to revolutionize the detection and management of tomato plant diseases. The data scientists and machine learning engineers develop and refine algorithms to accurately identify diseases from images, while the plant pathologist ensures scientific accuracy. Farmers provide practical insights, shaping actionable solutions. The team's collaborative approach blends technology with agricultural expertise, continuously innovating to offer a user-friendly tool for farmers and gardeners. We are dedicated to supporting healthier, more productive tomato crops and are open to collaboration and inquiries.

            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Contact Us
        st.markdown("<div class='section-header'>Contact Us</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='contact-info'>
            <p>For any inquiries or support, please reach out to us:</p>
            <ul>
                <li><strong>Email:</strong> <a href="mailto:support@tomatodiseaseclassifier.com">support@tomatodiseaseclassifier.com</a></li>
                <li><strong>Phone:</strong> +234-7064206404</li>
                <li><strong>Address:</strong> PMB 704, Ondo State, Nigeria</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Additional Information
        st.markdown("<div class='section-header'>Additional Information</div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class='section-content'>
            <p>We are constantly working to enhance our system's capabilities and to provide more value to our users. Follow us on our social media channels for updates and tips on plant health. \ntwitter: @DAVISCHOICE4 \nFacebook: @david.omeiza.92</p>
            </div>
            """,
            unsafe_allow_html=True
        )

elif app_mode == "FAQ":
      # Custom styling for FAQ section
      st.markdown(
          """
          <style>
          .faq-section {
              background-color: #f9f9f9;
              padding: 20px;
              border-radius: 10px;
              box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
          }
          .faq-header {
              color: #ff6347;
              text-align: center;
              font-size: 28px;
              margin-bottom: 15px;
              font-weight: bold;
          }
          .faq-item {
              background-color: #ffffff;
              padding: 15px;
              margin-bottom: 10px;
              border-radius: 8px;
              box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
          }
          .faq-question {
              color: #2e8b57;
              font-weight: bold;
              font-size: 18px;
          }
          .faq-answer {
              color: #555555;
              font-size: 16px;
              margin-top: 5px;
          }
          </style>
          """,
          unsafe_allow_html=True
      )

      # FAQ Header
      st.markdown("<h2 class='faq-header'>Frequently Asked Questions (FAQ)</h2>", unsafe_allow_html=True)

      # FAQ Items
      faqs = [
          {
              "question": "1. How do I use the Tomato Disease Classification System?",
              "answer": "To use the system, simply upload an image of your tomato plant leaf or take a picture using the built-in camera feature. The system will analyze the image and provide you with a diagnosis of the disease and suggested solutions."
          },
          {
              "question": "2. What types of tomato diseases can the system detect?",
              "answer": "The system can detect a variety of tomato diseases, including bacterial spot, early blight, late blight, and southern blight. It also provides solutions to manage these diseases effectively."
          },
          {
              "question": "3. Is there a way to save my prediction results?",
              "answer": "Yes, all your predictions are automatically saved in the database. You can view your past predictions and their details in the database if you are logged in."
          },
          {
              "question": "4. How do I register and log in to the system?",
              "answer": "To register, go to the Registration page and fill in your details. After registration, you can log in using your username and password. If you already have an account, use the Login page to access the system."
          },
          {
              "question": "5. What should I do if I encounter any issues or need support?",
              "answer": "For any issues or support, you can contact us via email at support@tomatodiseaseclassifier.com or call us at +234-7064206404. We are here to help you with any questions or concerns."
          }
      ]

      # Display FAQ Items
      for faq in faqs:
          with st.container():
              st.markdown(f"<div class='faq-item'><p class='faq-question'>{faq['question']}</p><p class='faq-answer'>{faq['answer']}</p></div>", unsafe_allow_html=True)
