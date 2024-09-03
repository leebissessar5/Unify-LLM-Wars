import streamlit as st
from unify import ChatBot


def update_credits() -> None:
    """
    Updates the credits in the session state
    """
    st.session_state["credits"] = st.session_state["LLM1"]._get_credits()


def clear_chats(*chatbots) -> None:
    """
    Clears the chat history of all chatbots

    Args:
        *chatbots (Chatbot): The chatbots whose chat history should be cleared
    """
    for chatbot in chatbots:
        chatbot._message_history = []


def create_chatbot_system_prompt(chatbot1: str, chatbot2: str) -> str:
    """
    Creates the system prompt for the battling chatbots

    Args:
        chatbot1 (str): The first chatbot
        chatbot2 (str): The second chatbot

    Returns:
        str: The system prompt for the battle
    """
    system_prompt = f"""
    You are {chatbot1} competing against {chatbot2} in a battle of wits and
     knowledge. When it's your turn as the first player of the round, ask a
     challenging technical question that would test your opponent's knowledge
     and skills. The second player will answer the question and you will
     evaluate the response before a judge selects the winner. The judge will
     determine the winner based on the accuracy, relevance, and depth of
     the response.
    """
    return system_prompt


def init_chatbots(chatbot1: str, chatbot2: str, judge: str) -> None:
    """
    Sets the system prompt accordingly for the chatbots

    Args:
        chatbot1 (str): The first chatbot
        chatbot2 (str): The second chatbot
        judge (str): The judge
    """
    judge_system_prompt = """You are the judge in an AI battle between two
     chatbots: LLM 1 and LLM 2. Your role is to critically evaluate the
     questions and answers provided, offering insightful commentary and
     declaring a winner based on the criteria of accuracy, relevance, and
     depth of response. After judging, state in the final line who is the
     winner, *exactly* like this: **Winner: LLM 1**"""

    chatbot1._update_message_history(
        role="system", content=create_chatbot_system_prompt("LLM 1", "LLM 2")
    )
    chatbot2._update_message_history(
        role="system", content=create_chatbot_system_prompt("LLM 2", "LLM 1")
    )
    judge._update_message_history(role="system", content=judge_system_prompt)


def battle_prompt(
    first_player: str,
    second_player: str,
) -> str:
    """
    Creates a battle prompt for the current round, including information
    about the previous rounds' results.

    Args:
        first_player (str): The first chatbot.
        second_player (str): The second chatbot.

    Returns:
        str: The battle prompt for the current round.
    """
    # Get the previous round results to provide context
    battle_results = st.session_state.get("battle_results", {})

    prompt = (
        f"Round {st.session_state['round_number']}: {first_player}, "
        "it's your turn to ask a question.\n"
    )

    # Add battle results if any rounds have been completed
    if st.session_state["round_number"] > 1:
        prompt += (
            f"""So far, you have {battle_results.get(
                f'{first_player} wins',
                0
            )} wins, """
            f"""and {battle_results.get(
                f'{second_player} wins',
                0
            )} wins for {second_player}. """
            f"There have been {battle_results.get('ties', 0)} ties."
        )

    return prompt


def llm_battle(
    chatbot1: ChatBot,
    chatbot2: ChatBot,
    judge: ChatBot,
    new_chat: bool = True,
    next_round: bool = True,
) -> None:
    """
    Simulates a battle between two chatbots

    Args:
        chatbot1 (Chatbot): The first chatbot
        chatbot2 (Chatbot): The second chatbot
        judge (Chatbot): The judge chatbot
        new_chat (bool, optional): Whether to start a new chat.
        Defaults to True.
        next_round (bool, optional): Whether to start the next round.
        Defaults to True.
    """
    if new_chat:
        clear_chats(chatbot1, chatbot2, judge)
        init_chatbots(chatbot1, chatbot2, judge)
        st.session_state["round_number"] = 1
        st.session_state["prev_content"] = []
        st.session_state["battle_results"] = {}
    else:
        if next_round:
            st.session_state["round_number"] += 1

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
        if content["Result"] in ["LLM 1 wins!", "LLM 2 wins!"]:
            st.success(content["Result"])
        else:
            st.info(content["Result"])
        st.markdown(content["Summary"])

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

        round_info = f"""*Round {st.session_state['round_number']}*,
        First player's turn: {
            'LLM 1' if st.session_state['round_number'] % 2 == 1 else 'LLM 2'
        }"""
        st.markdown(round_info)

        prompt = battle_prompt(first_player, second_player)

        with st.chat_message(first_player[-1]):
            player1_question = st.write_stream(
                chatbots[0]._process_input(
                    prompt, show_credits=False, show_provider=False
                )
            )

        with st.chat_message(second_player[-1]):
            player2_answer = st.write_stream(
                chatbots[1]._process_input(
                    f"""{first_player}'s question to you, {second_player}:
                     {player1_question}""",
                    show_credits=False,
                    show_provider=False,
                )
            )

        with st.chat_message(first_player[-1]):
            player1_evaluation = st.write_stream(
                chatbots[0]._process_input(
                    f"Evaluate {second_player}'s answer: {player2_answer}",
                    show_credits=False,
                    show_provider=False,
                )
            )

        with st.chat_message("Judge"):
            judge_evaluation = st.write_stream(
                judge._process_input(
                    f"""{first_player}'s Question: {player1_question}\n
                {second_player}'s Answer: {player2_answer}\n
                {first_player}'s Evaluation of {second_player}:
                 {player1_evaluation}""",
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
            st.session_state["battle_results"]["LLM 1 wins"] = (
                st.session_state["battle_results"].get("LLM 1 wins", 0) + 1
            )
        elif "Winner: LLM 2" in judge_evaluation:
            st.success("LLM 2 wins!")
            st.session_state["prev_content"][-1]["Result"] = "LLM 2 wins!"
            st.session_state["battle_results"]["LLM 2 wins"] = (
                st.session_state["battle_results"].get("LLM 2 wins", 0) + 1
            )
        else:
            st.info("It's a tie!")
            st.session_state["prev_content"][-1]["Result"] = "It's a tie!"
            st.session_state["battle_results"]["ties"] = (
                st.session_state["battle_results"].get("ties", 0) + 1
            )
        st.session_state["prev_content"][-1][
            "Summary"
        ] = f"""Round {st.session_state['round_number']}:
         LLM 1 wins: {st.session_state['battle_results'].get('LLM 1 wins', 0)},
         LLM 2 wins: {st.session_state['battle_results'].get('LLM 2 wins', 0)},
         ties: {st.session_state['battle_results'].get('ties', 0)}"""
        st.markdown(st.session_state["prev_content"][-1]["Summary"])

        update_credits()

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "Next Round",
            key=f"next{st.session_state['round_number']}",
            on_click=lambda: st.session_state["next_round_cb"](True),
        )

    with col2:
        st.button(
            "New Chat",
            key="new_chat",
            on_click=st.session_state["new_chat_cb"]
        )
