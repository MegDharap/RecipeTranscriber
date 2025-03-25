# Without streaming

import streamlit as st
from google import genai
from google.genai import types
from streamlit.components.v1 import html

# Function to call Gemini API given a video URL
def get_gemini_response(URL, api_key):
    client = genai.Client(
        api_key=api_key,
    )
    generate_content_config = types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        top_k=64,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )
    response = client.models.generate_content(
        model = "gemini-2.0-pro-exp-02-05",
        config = generate_content_config,
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=URL,
                        mime_type="video/*",
                    ),
                    types.Part.from_text(text="""Accurately and carefully EXTRACT ALL the ON-SCREEN TEXT *and* the FULL RECIPE from this video, in GitHub-compatible MARKDOWN, preserving all the timestamps and the text formatting:"""),
                ],
            ),
            types.Content(
                role="model",
                parts=[
                    types.Part.from_text(text="""Okay, here's the complete on-screen text and the full recipe, rendered using perfect Markdown syntax, with timestamps and formatting preserved:"""),
                ],
            ),
        ]
    )
    return(response.text)

# Streamlit UI
st.set_page_config(page_title="Recipe Transcriber | Pepper Content", page_icon="🍽️")
st.title('Recipe Transcriber | Pepper Content')
st.write("Drop the URL of a YouTube recipe video below to get Pepper's transcription of the full recipe!")

# Input from user
URL = st.text_input("What's the video URL?")

# Button to trigger the API call
if st.button('Get Transcript'):
    with st.spinner("Analysing and transcribing your video...", show_time=False):
        # Call the API and get the response
        api_key = st.secrets["GEMINI_API_KEY"]
        assistant_message = get_gemini_response(URL, api_key)
    
    # Display the text output
    st.markdown(assistant_message)
