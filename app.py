import streamlit as st

# Function to input API keys and endpoints
def input_fields():
    with st.sidebar:
        st.header("Configuration")
        unify_api_key = st.text_input("Unify API Key*", type="password", placeholder="Enter Unify API Key")
        endpoint1 = st.text_input("Endpoint 1*", placeholder="model@provider", value="gpt-3.5-turbo@openai")
        endpoint2 = st.text_input("Endpoint 2*", placeholder="model@provider", value="mixtral-8x7b-instruct-v0.1@together-ai")
        show_credits = st.toggle("Show Credit Usage", value=False)
        return unify_api_key, endpoint1, endpoint2, show_credits

# Function to display chat interface
def chat_interface():    
    # Display chat messages from history
    for message in st.session_state.messages:
        if message['role'] == 'user':
            with st.chat_message("User", avatar='🧑‍💻'):
                st.markdown(message['content'])
        elif message['role'] == 'ai':
            dual_chat = st.columns(2)
            with dual_chat[0].chat_message("AI 1", avatar='🤖'):
                st.markdown(message['content'][0])
            with dual_chat[1].chat_message("AI 2", avatar='🤖'):
                st.markdown(message['content'][1])

def main():
    st.set_page_config(page_title="LLM Wars", page_icon=":tada:", layout="wide")
    st.title("LLM Wars")

    placeholder = st.empty()
    placeholder.write('''
        Usage: 
        1. Input your **Unify API Key.** If you don’t have one yet, log in to the [console](https://console.unify.ai/) to get yours.
        2. Input your Endpoints (i.e. **Model and Provider ID** as model@provider). You can find both in the [benchmark interface](https://unify.ai/hub).
        3. Chat Away!
    ''')

    unify_api_key, endpoint1, endpoint2, show_credits = input_fields()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if user_input := st.chat_input("Type your message here..."):
        if unify_api_key and endpoint1 and endpoint2:
            placeholder.empty()
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            ai_response1 = "AI 1 says Hello!"
            ai_response2 = "AI 2 also says Hello!"
            st.session_state.messages.append({"role": "ai", "content": [ai_response1, ai_response2]})
            
            chat_interface()
        else:
            st.sidebar.warning("Please enter the Unify API Key and Endpoints to proceed.")

if __name__ == "__main__":
    main()