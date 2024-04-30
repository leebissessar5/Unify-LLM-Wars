import streamlit as st
from unify import ChatBot
from battle import llm_battle, update_credits
from config import input_fields


def init_session_state() -> None:
    '''
    Initialize the session state variables
    '''
    # Dictionary to define default values for session state keys
    defaults = {
        "LLM1": None,
        "LLM2": None,
        "Judge": None,
        "New Chat": True,
        "Done": None,
        "Next Round": None,
        "Valid Key": False,
        "previous_api_key": None,
        "new_chat_cb": new_chat_cb,
        "next_round_cb": next_round_cb,
        "prev_content": [],
        "battle_results": {},
        "round_number": 1,
        "prompt": "",
    }

    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def new_chat_cb() -> None:
    '''
    Callback function for the "New Chat" button
    '''
    st.session_state["New Chat"] = True
    st.session_state["Done"] = True


def next_round_cb(yes: bool) -> None:
    '''
    Callback function for the "Next Round" button

    Args:
        yes (bool): True if the user wants to start the next round,
        False otherwise
    '''
    st.session_state["Next Round"] = yes


def chatbots_exists() -> bool:
    '''
    Returns True if all chatbots are not None

    Returns:
        bool: True if all chatbots are not None
    '''
    return (
        st.session_state["LLM1"]
        and st.session_state["LLM2"]
        and st.session_state["Judge"]
    )


def chatbots_empty() -> bool:
    '''
    Returns True if all chatbots have no messages in their message history

    Returns:
        bool: True if all chatbots have no messages in their message history
    '''
    return chatbots_exists() and (
        not st.session_state["LLM1"]._message_history
        or not st.session_state["LLM2"]._message_history
        or not st.session_state["Judge"]._message_history
    )


def main():
    '''
    Main function for the app
    '''
    init_session_state()
    st.set_page_config(page_title="LLM Wars")
    st.title("LLM Wars &#x2694;")

    api_key, endpoints = input_fields()

    # Check if the API key has changed
    if api_key != st.session_state["previous_api_key"]:
        st.session_state["previous_api_key"] = api_key
        st.session_state["Valid Key"] = False  # Reset valid key state
        # erase chatbots
        for key in ["LLM1", "LLM2", "Judge"]:
            st.session_state[key] = None
        st.rerun()  # Rerun the app to revalidate the new API key

    # verify that all required fields are filled in
    if api_key and endpoints and all(endpoints.values()):
        # create ChatBot instances if they don't exist yet
        for keys in endpoints:
            if (
                not st.session_state[keys]
                or st.session_state[keys].endpoint != endpoints[keys]
            ):
                st.session_state[keys] = ChatBot(api_key, endpoints[keys])
                # Reset the chat if any of the ChatBots have been created
                st.session_state["New Chat"] = True

        try:
            update_credits()
            st.session_state["Valid Key"] = True
        except Exception:
            st.session_state["Valid Key"] = False

    # create empty placeholders for the instructions and start button
    placeholder, btn_placeholder = st.empty(), st.empty()
    # Show instructions if no ChatBots exist yet or the chat history is fresh
    if st.session_state["New Chat"]:
        placeholder.write(
            """
            Usage:
            1. Input your **Unify API Key**.  If you don’t have one yet,
             log in to the [console](https://console.unify.ai/) to get yours.
            2. Choose your Endpoints (i.e. **Model and Provider**,
             in the [benchmark interface](https://unify.ai/hub)).
            3. Click **Start Battle**.
        """
        )

        # show the start button only if the chat is fresh
        if btn_placeholder.button("Start Battle"):
            if st.session_state["Valid Key"]:
                if chatbots_exists():
                    placeholder.empty()
                    btn_placeholder.empty()
                    st.session_state["New Chat"] = False
                    llm_battle(
                        st.session_state["LLM1"],
                        st.session_state["LLM2"],
                        st.session_state["Judge"],
                        new_chat=True,
                    )
                else:
                    st.warning(
                        "Please enter the Unify API Key on the sidebar."
                    )
            else:
                st.error("Invalid key. Please check your Unify API Key.")
    else:
        llm_battle(
            st.session_state["LLM1"],
            st.session_state["LLM2"],
            st.session_state["Judge"],
            new_chat=False,
            next_round=st.session_state["Next Round"],
        )

    if st.session_state["Done"]:
        st.session_state["Done"] = False
        st.rerun()


if __name__ == "__main__":
    main()
