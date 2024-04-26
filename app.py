import streamlit as st
from unify import Unify
import requests
import json

# Load models and providers from JSON
with open('models.json', 'r') as f:
    data = json.load(f)
    models = data['models']

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

    def _get_credits(self):
        """Retrieve the credit balance using the Unify API."""
        url = 'https://api.unify.ai/v0/get_credits'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['credits']
        else:
            return f"Error fetching credits: {response.json().get('error', 'Unknown error')}"

def input_fields(selected_models):
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("API Key*", type="password")
        show_credits = st.checkbox("Show Credit Usage", value=False)

        model_names = [model['name'] for model in models if model['name'] not in selected_models]
        endpoints = {}

        for key in ["LLM1", "LLM2", "Judge"]:
            selected_model = st.selectbox(f"{key} Model", options=model_names, key=f"{key}_model")
            if selected_model:
                selected_models.append(selected_model)
                providers = [model['providers'] for model in models if model['name'] == selected_model][0]
                selected_provider = st.selectbox(f"{key} Provider", options=providers, key=f"{key}_provider")
                endpoints[key] = f"{selected_model}@{selected_provider}"

        return api_key, endpoints, show_credits

def llm_battle(chatbot1, chatbot2, judge, show_credits):
    prompt = "Generate a random question that you need to get answered."
    round_number = 1

    while True:
        question = chatbot1.send_message(prompt)
        answer_llm2 = chatbot2.send_message(question)
        evaluation_llm1 = chatbot1.send_message(f"Evaluating LLM2's response: {answer_llm2}")
        answer_llm1 = chatbot1.send_message(question)

        judge_response = judge.send_message(f"Judge the responses: Original Question: {question}\nLLM2's Answer: {answer_llm2}\nLLM1's Evaluation of LLM2: {evaluation_llm1}\nLLM1's Answer: {answer_llm1}")

        st.write(f"Round {round_number}:")
        st.markdown(f"*LLM1 Question:* {question}")
        st.markdown(f"*LLM2's Answer:* {answer_llm2}")
        st.markdown(f"*LLM1's Evaluation of LLM2:* {evaluation_llm1}")
        st.markdown(f"*LLM1's Answer:* {answer_llm1}")
        st.markdown(f"*Judge's Evaluation:* {judge_response}")

        if show_credits:
            credits = chatbot1._get_credits()
            st.sidebar.write(f"Credit Balance: ${credits}")

        if not st.button("Next Round", key=f"next{round_number}"):
            break

        round_number += 1
        prompt = "Generate another random question."

def main():
    st.title("LLM Wars &#x2694;")
    selected_models = []
    api_key, endpoints, show_credits = input_fields(selected_models)

    if api_key and endpoints and all(endpoints.values()):
        chatbot1 = ChatBot(api_key, endpoints['LLM1'])
        chatbot2 = ChatBot(api_key, endpoints['LLM2'])
        judge = ChatBot(api_key, endpoints['Judge'])

        if st.button("Start Battle"):
            llm_battle(chatbot1, chatbot2, judge, show_credits)

if __name__ == "__main__":
    main()