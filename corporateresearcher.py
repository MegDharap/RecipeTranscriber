import streamlit as st
import requests
import json
from streamlit.components.v1 import html

# Function to call Perplexity API given a company name
def query_perplexity(COMPANY, INDUSTRY, api_key):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "llama-3.1-sonar-huge-128k-online",
        "messages": [
            {
                "role": "system",
                "content": f"""You are an expert corporate researcher with in-depth knowledge of the global {INDUSTRY} industry. You are answering my query IN DEPTH, using ONLY RELIABLE and RECENT search results from credible industry sources or official company websites. You will proceed step by step to write a COMPREHENSIVE MULTI-SECTION answer containing a DETAILED LIST for EACH point in my query.
                
                You will GO DEEP to identify ALL the key details about the company {COMPANY} from highly reliable {INDUSTRY} industry sources. You'll conduct NUMEROUS searches until you have comprehensive and deep info that covers everything any B2B sales lead researcher could want to know about {COMPANY}. You will then give me a complete, highly granular, detailed, reliable, fact-checked list of everything my query asks for, and ALL other useful info you can find.
                
                You must ALWAYS CITE YOUR SOURCES, with numbered in-line references in the format [1], [2], and so on. You ENSURE you MATCH these with a FULL REFERENCE LIST providing ALL YOUR FULL, CORRECT SOURCE URLs at the bottom of your answer, in this format:
                
                References:
                [1] [Insert SOURCE URL 1]
                [2] [Insert SOURCE URL 2]
                ... and so on, until ALL URLs you used are correctly mentioned!"""
            },
            {
                "role": "user",
                "content": f"What are the main offerings, operational processes, organisational goals, challenges, digital transformation goals, industry trends, technology infrastructure and competitive edge of {COMPANY}?"
            }
        ],
        "max_tokens": 2000,
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
st.set_page_config(page_title="Corporate Researcher", page_icon="🔎")
st.title('Corporate Researcher')

# Input from user
COMPANY = st.text_input("Name the company you are researching.")
INDUSTRY = st.text_input("Which industry are you targeting?")

# Button to trigger the API call
if st.button('Research Company'):
    # Call the API and get the response
    api_key = st.secrets["PERPLEXITY_API_KEY"]
    assistant_message = query_perplexity(COMPANY, INDUSTRY, api_key)
    
    # Display the text output
    st.text_area("Here's the key information about the company:", assistant_message, height=750)
