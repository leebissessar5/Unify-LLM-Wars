import streamlit as st


def update_credits() -> None:
    '''
    Updates the credits in the session state
    '''
    st.session_state["credits"] = st.session_state["LLM1"]._get_credits()


def clear_chats(*chatbots) -> None:
    '''
    Clears the chat history of all chatbots

    Args:
        *chatbots (Chatbot): The chatbots whose chat history should be cleared
    '''
    for chatbot in chatbots:
        chatbot._message_history = []


def llm_battle(chatbot1, chatbot2, judge, new_chat=True, next_round=True):
    '''
    Simulates a battle between two chatbots

    Args:
        chatbot1 (Chatbot): The first chatbot
        chatbot2 (Chatbot): The second chatbot
        judge (Chatbot): The judge chatbot
        new_chat (bool, optional): Whether to start a new chat.
        Defaults to True.
        next_round (bool, optional): Whether to start the next round.
        Defaults to True.
    '''
    if new_chat:
        clear_chats(chatbot1, chatbot2, judge)
        st.session_state["round_number"] = 1
        st.session_state["prompt"] = (
            "Generate a random question that you need to get answered, without giving an answer yourself."
        )
        st.session_state["prev_content"] = []
    else:
        if next_round:
            st.session_state["round_number"] += 1
        st.session_state["prompt"] = (
            "Generate another random question that you need to get answered, without giving an answer yourself."
        )

    for content in st.session_state["prev_content"]:
        st.markdown(content["Info"])
        with st.chat_message(content["P1"][-1]):
            st.write(content["P1 Q"])
        with st.chat_message(content["P2"][-1]):
            st.write(content["P2 A"])
        with st.chat_message(content["P1"][-1]):
            st.write(content["P1 Eval"])
        with st.chat_message("Judge"):
            st.write(content["Judge Eval"])
        st.markdown(content["Result"])

    if next_round:
        st.session_state["next_round_cb"](False)
        chatbots = (
            (chatbot1, chatbot2)
            if st.session_state["round_number"] % 2 == 1
            else (chatbot2, chatbot1)
        )
        first_player, second_player = (
            ("LLM 1", "LLM 2")
            if st.session_state["round_number"] % 2 == 1
            else ("LLM 2", "LLM 1")
        )

        round_info = f"*Round {st.session_state['round_number']}*, First player's turn: {'LLM 1' if st.session_state['round_number'] % 2 == 1 else 'LLM 2'}"
        st.markdown(round_info)

        with st.chat_message(first_player[-1]):
            player1_question = st.write_stream(
                chatbots[0]._process_input(
                    st.session_state["prompt"], show_credits=False, show_provider=False
                )
            )

        with st.chat_message(second_player[-1]):
            player2_answer = st.write_stream(
                chatbots[1]._process_input(
                    player1_question, show_credits=False, show_provider=False
                )
            )

        with st.chat_message(first_player[-1]):
            player1_evaluation = st.write_stream(
                chatbots[0]._process_input(
                    f"Evaluating {second_player}'s answer: {player2_answer}",
                    show_credits=False,
                    show_provider=False,
                )
            )

        with st.chat_message("Judge"):
            judge_evaluation = st.write_stream(
                judge._process_input(
                    f"""Judge the responses: {first_player}'s Question: {player1_question}\n
                {second_player}'s Answer: {player2_answer}\n
                {first_player}'s Evaluation of {second_player}: {player1_evaluation}\n
                After judging, state in the final line who is the winner, *exactly* like this: **Winner: LLM 1**""",
                    show_credits=False,
                    show_provider=False,
                )
            )

        st.session_state["prev_content"].append(
            {
                "Info": round_info,
                "P1": first_player,
                "P2": second_player,
                "P1 Q": player1_question,
                "P2 A": player2_answer,
                "P1 Eval": player1_evaluation,
                "Judge Eval": judge_evaluation,
            }
        )

        if "Winner: LLM 1" in judge_evaluation:
            st.success("LLM 1 wins!")
            st.session_state["prev_content"][-1]["Result"] = "LLM 1 wins!"
        elif "Winner: LLM 2" in judge_evaluation:
            st.success("LLM 2 wins!")
            st.session_state["prev_content"][-1]["Result"] = "LLM 2 wins!"
        else:
            st.info("It's a tie!")
            st.session_state["prev_content"][-1]["Result"] = "It's a tie!"

        update_credits()

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Next Round",
            key=f"next{st.session_state['round_number']}",
            on_click=lambda: st.session_state["next_round_cb"](True),
        )

    with col2:
        st.button("New Chat", key=f"new_chat", on_click=st.session_state["new_chat_cb"])
