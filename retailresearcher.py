import streamlit as st
import requests
import json
from streamlit.components.v1 import html

# Function to call Perplexity API given a product name
def query_perplexity(product_name, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar-medium-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a US-based retail expert familiar with the full inventory of Walmart, Target, Instacart, Kroger, Amazon, etc. You will seek complete, highly reliable details about the given Product using ONLY the official manufacturer's website and top-ranking Retailer websites, and provide me with ALL the product details available. You will proceed step by step to write a COMPREHENSIVE MULTI-SECTION answer containing a DETAILED LIST for EACH point in my query. Cite your source TITLES at the end like this: \n Sources: <FULL Source 1 website name and title> \n <FULL Source 2 website name and title> . . . and so on."
            },
            {
                "role": "user",
                "content": f"What are the ingredients, label info, highlights, description, nutrition information, allergens, specifications, uses, features, attributes, directions of use, storage instructions, serving suggestions, etc. of {product_name}?"
            }
        ],
        "max_tokens": 2000,
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 0,
        "presence_penalty": 0,
        "frequency_penalty": 0.2
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    return response_data['choices'][0]['message']['content']

# Streamlit UI
st.title('General Mills Retail Researcher')

# Input from user
product_name_input = st.text_input("Name the product you are researching.")

# Button to trigger the API call
if st.button('Research Product'):
    # Call the API and get the response
    api_key = st.secrets["PERPLEXITY_API_KEY"]
    assistant_message = query_perplexity(product_name_input, api_key)
    
    # Display the text output
    st.text_area("Here's the key information about the product:", assistant_message, height=750)
