import streamlit as st
from unify import ChatBot
from battle import llm_battle
from config import input_fields

for key in ['LLM1', 'LLM2', 'Judge', 'New Chat', 'Done']:
    if key not in st.session_state:
        st.session_state[key] = None

def new_chat_cb():
    st.session_state['New Chat'] = True
    st.session_state['Done'] = True

def chatbots_exists():
    return st.session_state['LLM1'] and st.session_state['LLM2'] and st.session_state['Judge']

def chatbots_empty():
    return chatbots_exists() and (not st.session_state['LLM1']._message_history \
             or not st.session_state['LLM2']._message_history \
             or not st.session_state['Judge']._message_history)

def main():
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars &#x2694;")

    api_key, endpoints, show_credits = input_fields()

    if 'new_chat_cb' not in st.session_state:
        st.session_state['new_chat_cb'] = new_chat_cb

    # verify that all required fields are filled in
    if api_key and endpoints and all(endpoints.values()):
        # create ChatBot instances if they don't exist yet
        for keys in endpoints:
            if not st.session_state[keys] or st.session_state[keys].endpoint != endpoints[keys]:
                st.session_state[keys] = ChatBot(api_key, endpoints[keys])
                # Reset the chat if any of the ChatBots have been created
                st.session_state['New Chat'] = True

    # create empty placeholders for the instructions and start button
    placeholder, btn_placeholder = st.empty(), st.empty()
    # Show instructions if no ChatBots exist yet or the chat history is fresh
    if st.session_state['New Chat']:
        placeholder.write('''
            Usage: 
            1. Input your **Unify API Key** (if not stored as secrets, use the sidebar). If you don’t have one yet, log in to the [console](https://console.unify.ai/) to get yours.
            2. Choose your Endpoints (i.e. **Model and Provider**, in the [benchmark interface](https://unify.ai/hub)).
            3. Click **Start Battle**.
        ''')

        # show the start button only if the chat is fresh
        if btn_placeholder.button("Start Battle"):
            if chatbots_exists():
                placeholder.empty()
                btn_placeholder.empty()
                st.session_state['New Chat'] = False
                llm_battle(st.session_state['LLM1'], st.session_state['LLM2'], st.session_state['Judge'], show_credits, new_chat=True)
            else:
                st.warning("Please enter the Unify API Key on the sidebar to proceed.")
    else:
        llm_battle(st.session_state['LLM1'], st.session_state['LLM2'], st.session_state['Judge'], show_credits, new_chat=False)

    if st.session_state['Done']:
        st.session_state['Done'] = False
        st.rerun()


if __name__ == "__main__":
    main()