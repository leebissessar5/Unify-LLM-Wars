import streamlit as st
from unify import ChatBot

# Function to input API keys and endpoints
def input_fields():
    with st.sidebar:
        st.header("Configuration")
        unify_api_key = st.text_input("Unify API Key*", type="password", placeholder="Enter Unify API Key")
        endpoint1 = st.text_input("Endpoint 1*", placeholder="model@provider", value="claude-3-haiku@anthropic")
        endpoint2 = st.text_input("Endpoint 2*", placeholder="model@provider", value="mixtral-8x7b-instruct-v0.1@together-ai")
        show_credits = st.toggle("Show Credit Usage", value=False)
        return unify_api_key, endpoint1, endpoint2, show_credits

# Function to display chat interface
def chat_interface(prompt, chatbot1, chatbot2):    
    # Display chat messages from history
    for msg1, msg2 in zip(chatbot1._message_history, chatbot2._message_history):
        # both chatbots recieve the same user input
        if msg1['role'] == 'user':
            with st.chat_message("User", avatar='🧑‍💻'):
                st.markdown(msg1['content'])
        elif msg1['role'] == 'assistant':
            dual_chat = st.columns(2)
            with dual_chat[0].chat_message("AI 1", avatar='🤖'):
                st.markdown(msg1['content'])
            with dual_chat[1].chat_message("AI 2", avatar='🤖'):
                st.markdown(msg2['content'])

    # stream the current prompt
    with st.chat_message("User", avatar='🧑‍💻'):
        st.markdown(prompt)
    dual_chat = st.columns(2)
    with dual_chat[0].chat_message("AI 1", avatar='🤖'):
        st.write_stream(chatbot1._process_input(prompt, show_credits=False, show_provider=False))
    with dual_chat[1].chat_message("AI 2", avatar='🤖'):
        st.write_stream(chatbot2._process_input(prompt, show_credits=False, show_provider=False))

def main():
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars")

    placeholder = st.empty()
    placeholder.write('''
        Usage: 
        1. Input your **Unify API Key.** If you don’t have one yet, log in to the [console](https://console.unify.ai/) to get yours.
        2. Input your Endpoints (i.e. **Model and Provider ID** as model@provider). You can find both in the [benchmark interface](https://unify.ai/hub).
        3. Chat Away!
    ''')

    chatbot1, chatbot2 = None, None

    unify_api_key, endpoint1, endpoint2, show_credits = input_fields()
    ready = unify_api_key and endpoint1 and endpoint2

    if ready:
        chatbot1 = ChatBot(unify_api_key, endpoint1)
        chatbot2 = ChatBot(unify_api_key, endpoint2)
        if show_credits:
            st.sidebar.write(f"Credit Balance: ${chatbot1._get_credits():.2g}")

    if user_input := st.chat_input("Type your message here..."):
        if unify_api_key and endpoint1 and endpoint2:
            placeholder.empty()
            chat_interface(user_input, chatbot1, chatbot2)
        else:
            st.sidebar.warning("Please enter the Unify API Key and Endpoints to proceed.")

if __name__ == "__main__":
    main()