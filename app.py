import streamlit as st
from unify import ChatBot 

# Function to input API keys and endpoints
def input_fields():
    with st.sidebar:
        st.header("Configuration")
        unify_api_key = st.text_input("Unify API Key*", type="password", placeholder="Enter Unify API Key")
        endpoint1 = st.text_input("Endpoint 1*", placeholder="model@provider", value="llama-2-70b-chat@anyscale")
        endpoint2 = st.text_input("Endpoint 2*", placeholder="model@provider", value="mixtral-8x7b-instruct-v0.1@together-ai")
        return unify_api_key, endpoint1, endpoint2

# Function to create ChatBot objects and manage chat state
def main():
    st.set_page_config(page_title="LLM Wars", page_icon=":tada:", layout="wide")
    st.title("LLM Wars")
    
    st.write('''
	Usage: 
	1. Input your **Unify API Key.** If you don’t have one yet, log in to the [console](https://console.unify.ai/) to get yours.
	2. Input your Endpoints (i.e. **Model and Provider ID** as model@provider). You can find both in the [benchmark interface](https://unify.ai/hub).
	3. Chat Away!
	''')

    unify_api_key, endpoint1, endpoint2 = input_fields()

    if user_input := st.chat_input("Type your message here..."):
        if unify_api_key and endpoint1 and endpoint2:
            pass
        else:
            st.sidebar.warning("Please enter the Unify API Key and Endpoints to proceed.")


if __name__ == "__main__":
    main()
