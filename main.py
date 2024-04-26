import streamlit as st
from chatbot import ChatBot
from config import input_fields
from battle import llm_battle

def main():
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars &#x2694;")
    api_key, endpoints, show_credits = input_fields()

    if api_key and endpoints and all(endpoints.values()):
        chatbot1 = ChatBot(api_key, endpoints['LLM1'])
        chatbot2 = ChatBot(api_key, endpoints['LLM2'])
        judge = ChatBot(api_key, endpoints['Judge'])

        if st.button("Start Battle"):
            llm_battle(chatbot1, chatbot2, judge, show_credits)

if __name__ == "__main__":
    main()