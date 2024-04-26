import streamlit as st
import json

# Load models and providers from JSON
with open('models.json', 'r') as f:
    data = json.load(f)
    models = data['models']

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