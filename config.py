import streamlit as st
import json

# Load models and providers from JSON
with open('models.json', 'r') as f:
    data = json.load(f)
    models = data['models']

def input_fields():
    with st.sidebar:
        st.header("Configuration")

        # Show text field if API key is not stored in secrets
        if 'unify_api_key' in st.secrets:
            api_key = st.secrets['unify_api_key']
        else:
            api_key = st.text_input("Unify API Key*", type="password", placeholder="Enter Unify API Key")


        model_names = [model['name'] for model in models]
        endpoints = {}

        for key in ["LLM1", "LLM2", "Judge"]:
            selected_model = st.selectbox(f"{key} Model", options=model_names, key=f"{key}_model")
            if selected_model:
                providers = [model['providers'] for model in models if model['name'] == selected_model][0]
                selected_provider = st.selectbox(f"{key} Provider", options=providers, key=f"{key}_provider")
                endpoints[key] = f"{selected_model}@{selected_provider}"

        show_credits = st.toggle("Show Credit Usage", value=False)

        return api_key, endpoints, show_credits