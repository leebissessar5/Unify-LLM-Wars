import streamlit as st
import json
import requests
import time
from typing import List, Dict, Tuple

base_url = "https://api.unify.ai/v0"


def init_session_state() -> None:
    '''
    Initialize session state if it doesn't exist yet
    '''
    if 'selections' not in st.session_state:
        st.session_state['selections'] = {
            'LLM1': {}, 'LLM2': {}, 'Judge': {}
        }


@st.cache_data
def load_models() -> List[Dict[str, str]]:
    '''
    Load models from models.json

    Returns:
        List[Dict[str, str]]: List of models
    '''
    with open("models.json", "r") as f:
        data = json.load(f)
    return data["models"]


def get_providers(model: str) -> List[str]:
    '''
    Get providers for a given model

    Args:
        model (str): The model name

    Returns:
        List[str]: List of providers
    '''
    url = f"{base_url}/endpoints_of"
    response = requests.get(url, params={"model": model})
    if response.status_code == 200:
        providers = [provider.split("@")[1]
                     for provider in json.loads(response.text)]
        return providers
    else:
        st.error("Failed to fetch providers from API.")
        return []


def get_summary_string(key: str) -> str:
    """
    Generate summary string for the expander based on current selections.

    Args:
        key (str): The key for LLM1, LLM2, or Judge

    Returns:
        str: A formatted summary string
    """
    selection = st.session_state["selections"][key]
    if selection.get("name") and selection.get("provider"):
        return f"{key}: {selection['name']}@{selection['provider']}"
    return f"{key} Configuration"


def update_models() -> None:
    '''
    Update models.json with providers
    '''
    model_names = list_models()
    models = []

    if not model_names:
        st.error("No models found to update.")
        return

    progress_bar = st.progress(0)
    message_placeholder = st.empty()  # Placeholder for the message
    total_models = len(model_names)

    for index, model in enumerate(model_names):
        message_placeholder.text(f"Searching providers for {model}...")

        providers = get_providers(model)
        models.append({"name": model, "providers": providers})

        # Update the progress bar
        progress_bar.progress((index + 1) / total_models)

    with open("models.json", "w") as f:
        json.dump({"models": models}, f, indent=4)

    st.success("Models and providers updated successfully!")
    message_placeholder.empty()  # Clear the message placeholder


def list_models() -> List[str]:
    '''
    List models from Unify API

    Returns:
        List[str]: List of models
    '''
    url = f"{base_url}/models"
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        st.error("Failed to fetch models from API.")
        return []


def select_model_provider(key: str, models: List[Dict[str, str]]) -> str:
    """
    Render model and provider selection boxes and update session state.

    Args:
        key (str): The key for LLM1, LLM2, or Judge
        models (List[Dict[str, str]]): List of models and their providers

    Returns:
        str: The endpoint string constructed from selected model and provider
    """
    model_names = [model["name"] for model in models]
    selected_model = st.selectbox(
        "Model",
        options=model_names,
        key=f"{key}_model",
    )
    st.session_state["selections"][key]["name"] = selected_model

    if selected_model:
        model_details = next(
            (item for item in models if item["name"] == selected_model), None
        )
        if model_details:
            providers = model_details["providers"]
            selected_provider = st.selectbox(
                "Provider",
                options=providers,
                key=f"{key}_provider",
            )
            st.session_state["selections"][key]["provider"] = selected_provider
            return f"{selected_model}@{selected_provider}"
    return ""


def input_fields() -> Tuple[str, Dict[str, str]]:
    """
    Input fields for the app

    Returns:
        Tuple[str, Dict[str, str]]: API key, endpoints
    """
    init_session_state()
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input(
            "Unify API Key*",
            type="password",
            placeholder="Enter Unify API Key"
        )

        models = load_models()

        endpoints = {}
        for key in ["LLM1", "LLM2", "Judge"]:
            with st.expander(get_summary_string(key), expanded=False):
                endpoint = select_model_provider(key, models)
                if endpoint:
                    endpoints[key] = endpoint

        if st.session_state["Valid Key"] and st.sidebar.toggle(
         "Show Credit Balance", value=False, key='show_credit'
        ):
            if "credits" in st.session_state:
                st.sidebar.write(
                    f"Credit Balance: ${st.session_state['credits']:.2f}"
                )

        if st.button("Update Models from API"):
            update_models()
            time.sleep(1)  # Add a delay to indicate the update is complete
            st.rerun()

        return api_key, endpoints
