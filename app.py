import streamlit as st
from unify import Unify

class ChatBot:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.client = Unify(api_key=api_key, endpoint=endpoint)
        self.message_history = []

    def send_message(self, message):
        self.message_history.append({'role': 'user', 'content': message})
        try:
            response = self.client.generate(messages=self.message_history)
            self.message_history.append({'role': 'assistant', 'content': response})
            return response
        except Exception as e:
            return f"Error: {str(e)}"

def input_fields():
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("API Key*", type="password")
        endpoint1 = st.text_input("LLM1 Endpoint*", "claude-3-opus@anthropic")
        endpoint2 = st.text_input("LLM2 Endpoint*", "mixtral-8x7b-instruct-v0.1@mistral-ai")
        judge_endpoint = st.text_input("Judge Endpoint*", "llama-3-8b-chat@together-ai")
        return api_key, endpoint1, endpoint2, judge_endpoint

def llm_battle(chatbot1, chatbot2, judge):
    prompt = "Generate a random question that you need to get answered."
    round_number = 1

    while True:
        question = chatbot1.send_message(prompt)
        answer_llm2 = chatbot2.send_message(question)

        # LLM1 evaluates LLM2's response before providing its own answer
        evaluation_llm1 = chatbot1.send_message(f"Evaluating LLM2's response: {answer_llm2}")
        answer_llm1 = chatbot1.send_message(f"Here's my take on the question: {question}")

        # Judge evaluates both responses
        judge_response = judge.send_message(f"Judge the responses: Original Question: {question}\nLLM2's Answer: {answer_llm2}\nLLM1's Evaluation of LLM2: {evaluation_llm1}\nLLM1's Answer: {answer_llm1}")

        st.write(f"Round {round_number}:")
        st.markdown(f"*LLM1 Question:* {question}")
        st.markdown(f"*LLM2's Answer:* {answer_llm2}")
        st.markdown(f"*LLM1's Evaluation of LLM2:* {evaluation_llm1}")
        st.markdown(f"*LLM1's Answer:* {answer_llm1}")
        st.markdown(f"*Judge's Evaluation:* {judge_response}")

        # Determine winner based on judge's evaluation
        if "LLM1 wins" in judge_response:
            st.success("LLM1 wins this round!")
        elif "LLM2 wins" in judge_response:
            st.success("LLM2 wins this round!")
        else:
            st.info("No clear winner this round.")

        if not st.button("Next Round", key=f"next{round_number}"):
            break

        round_number += 1
        prompt = "Generate another random question."

def main():
    st.title("LLM Wars")
    api_key, endpoint1, endpoint2, judge_endpoint = input_fields()

    if api_key and endpoint1 and endpoint2 and judge_endpoint:
        chatbot1 = ChatBot(api_key, endpoint1)
        chatbot2 = ChatBot(api_key, endpoint2)
        judge = ChatBot(api_key, judge_endpoint)

        if st.button("Start Battle"):
            llm_battle(chatbot1, chatbot2, judge)

if __name__ == "__main__":
    main()