import streamlit as st
from chatbot import ChatBot
from config import input_fields
from battle import llm_battle

if 'LLM1' not in st.session_state:
    st.session_state['LLM1'] = None
if 'LLM2' not in st.session_state:
    st.session_state['LLM2'] = None

def chatbots_exists():
    return st.session_state['LLM1'] and st.session_state['LLM2'] and st.session_state['Judge']

def chatbots_empty():
    return (not st.session_state['LLM1']._message_history \
             or not st.session_state['LLM2']._message_history \
             or not st.session_state['Judge']._message_history)

def main():
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars &#x2694;")

    placeholder = st.empty()
    placeholder.write('''
            Usage: 
            1. Input your **Unify API Key** (if not stored as secrets, use the sidebar). If you don’t have one yet, log in to the [console](https://console.unify.ai/) to get yours.
            2. Choose your Endpoints (i.e. **Model and Provider**, in the [benchmark interface](https://unify.ai/hub)).
            3. Click **Start Battle**.
        ''')

    api_key, endpoints, show_credits = input_fields()

    # verify that all required fields are filled in
    if api_key and endpoints and all(endpoints.values()):
        st.session_state['LLM1'] = ChatBot(api_key, endpoints['LLM1'])
        st.session_state['LLM2'] = ChatBot(api_key, endpoints['LLM2'])
        st.session_state['Judge'] = ChatBot(api_key, endpoints['Judge'])

    if st.button("Start Battle"):
        if api_key and chatbots_exists():
            llm_battle(st.session_state['LLM1'], st.session_state['LLM2'], st.session_state['Judge'], show_credits)
        else:
            st.warning("Please enter the Unify API Key on the sidebar to proceed.")

if __name__ == "__main__":
    main()