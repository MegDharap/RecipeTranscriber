import streamlit as st
import requests
import json

# Function to call Perplexity API given a company name
def query_perplexity(company_name, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "pplx-70b-online",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert corporate researcher with in-depth knowledge of manufacturing, oil and gas, energy, utilities, and related industries. You are answering my queries using ONLY RELIABLE search results from credible industry sources or official company websites."
            },
            {
                "role": "user",
                "content": f"What are the main offerings, operational processes, organisational goals, challenges, digital transformation goals, industry trends, technology infrastructure and competitive edge of {company_name}? Answer step by step. Cite your source TITLES at the end like this: \n Sources: <FULL Source 1 website name and title> \n <FULL Source 2 website name and title> . . . and so on."
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.8,
        "top_p": 1,
        "top_k": 0,
        "presence_penalty": 0,
        "frequency_penalty": 1
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
st.title('Perplexity AI Corporate Researcher')

# Input from user
company_name_input = st.text_input("Name the company you are researching.")

# Button to trigger the API call
if st.button('Research Company'):
    # Call the API and get the response
    api_key = st.secrets["PERPLEXITY_API_KEY"]
    assistant_message = query_perplexity(company_name_input, api_key)
    
    # Display the text output
    st.text_area("Result", assistant_message, height=150)
    
    # Copy button
    if st.button('Copy'):
        st.experimental_set_query_params(clipboard=assistant_message)
        st.success("Text copied to clipboard!")