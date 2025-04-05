from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("YOUR_API_KEY"))  # Replace with your API key

def get_gemini_repsonse(input, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, prompt])
    return response.text

# Page settings
st.set_page_config(page_title="Crop Monitoring Tool", layout="centered")

# Inject custom CSS
st.markdown("""
    <style>
        body {
            background-color: #f9f9f2;
        }

        .main-container {
            background-color: white;
            padding: 0px 50px 30px 50px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 0px;
        }

        .header {
            background-color: #2ea44f;
            color: white;
            padding: 20px 30px;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            font-size: 24px;
            font-weight: bold;
            text-align: left;
            margin: -40px -50px 30px -50px;
        }

        label, .stTextInput, .stTextArea {
            margin-bottom: 20px;
        }

        /* Increase font size of labels */
        .stTextInput label, .stTextArea label {
            font-size: 20px !important;
            font-weight: 600;
        }

        /* Input field font size */
        .stTextInput>div>div>input,
        .stTextArea>div>textarea {
            font-size: 16px;
        }

        /* Analyze button style */
        .stButton button {
            background-color: #2ea44f !important;
            color: white !important;
            font-weight: bold;
            font-size: 16px;
            border-radius: 8px;
            height: 45px;
            width: 100%;
            margin-top: 20px;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Layout container
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="header">Crop Data Analysis Tool</div>', unsafe_allow_html=True)

# Input fields
crop_name = st.text_input("Crop Name", placeholder="e.g., Wheat, Rice, Cotton")
st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

data = st.text_area("Paste Crop Environmental Data (JSON or XML)", 
                    placeholder='{"temperature": 30, "humidity": 70, "soil_pH": 6.5, "sunlight": "moderate"}', 
                    height=150)
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Button
submit = st.button("Analyze Crop Data", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Gemini prompt
input_prompt = """
Act as a Senior Farmer and Environmental Scientist. I am giving you some data in JSON or XML format which represents the environment for a crop. 
Analyze it and tell whether it is suitable or not for the given crop.
Use simple language and show the result in tabular form with columns:
- Factor
- Environmental data
- Suitable Range
-Suitable?

Also give bullet-point suggestions and a conclusion.
The crop name is:
"""

input = input_prompt + crop_name + " and the data is: " + data

# Output
if submit:
    with st.spinner("Analyzing Crop Data..."):
        response = get_gemini_repsonse(input_prompt, input)
    st.subheader("Analysis Result:")
    st.write(response)
