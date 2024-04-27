import streamlit as st

round_number = 1
prompt = "Generate a random question that you need to get answered, without giving an answer yourself."
prev_content = []

def clear_chats(*chatbots):
    for chatbot in chatbots:
        chatbot._message_history = []

def llm_battle(chatbot1, chatbot2, judge, show_credits, new_chat=True):
    global round_number, prompt, prev_content

    if new_chat:
        clear_chats(chatbot1, chatbot2, judge)
        round_number = 1
        prompt = "Generate a random question that you need to get answered, without giving an answer yourself."
        prev_content = []
    else:
        round_number += 1
        prompt = "Generate another random question that you need to get answered, without giving an answer yourself."

    for content in prev_content:
        st.markdown(content['Info'])
        with st.chat_message("User", avatar='🧑‍💻'):
            st.write(content['Prompt'])
        with st.chat_message(content['P1'][-1]):
            st.write(content['P1 Q'])
        with st.chat_message(content['P2'][-1]):
            st.write(content['P2 A'])
        with st.chat_message(content['P1'][-1]):
            st.write(content['P1 Eval'])
        with st.chat_message('Judge'):
            st.write(content['Judge Eval'])
        st.markdown(f"**Winner:** {content['Winner']}")

    chatbots = (chatbot1, chatbot2) if round_number % 2 == 1 else (chatbot2, chatbot1)
    first_player, second_player = ('LLM 1', 'LLM 2') if round_number % 2 == 1 else ('LLM 2', 'LLM 1')

    round_info = f"*Round {round_number}*, First player's turn: {'LLM 1' if round_number % 2 == 1 else 'LLM 2'}"
    st.markdown(round_info)

    with st.chat_message(first_player[-1]):
        player1_question = st.write_stream(chatbots[0]._process_input(prompt, show_credits=False, show_provider=False))

    with st.chat_message(second_player[-1]):
        player2_answer = st.write_stream(chatbots[1]._process_input(player1_question, show_credits=False, show_provider=False))
    
    with st.chat_message(first_player[-1]):
        player1_evaluation = st.write_stream(chatbots[0]._process_input(f"Evaluating {second_player}'s answer: {player2_answer}", show_credits=False, show_provider=False))

    with st.chat_message('Judge'):
        judge_evaluation = st.write_stream(
            judge._process_input(f'''Judge the responses: {first_player}'s Question: {player1_question}\n
            {second_player}'s Answer: {player2_answer}\n
            {first_player}'s Evaluation of {second_player}: {player1_evaluation}\n
            After judging, state in the final line who is the winner, *exactly* like this: **Winner: LLM 1**''', 
            show_credits=False, show_provider=False)
        )

    prev_content.append(
        {
            'Info': round_info,
            'P1': first_player,
            'P2': second_player,
            'Prompt': prompt,
            'P1 Q': player1_question,
            'P2 A': player2_answer,
            'P1 Eval': player1_evaluation,
            'Judge Eval': judge_evaluation
        }
    )

    if "Winner: LLM 1" in judge_evaluation:
        st.success("LLM 1 wins!")
        prev_content[-1]['Winner'] = 'LLM 1'
    elif "Winner: LLM 2" in judge_evaluation:
        st.success("LLM 2 wins!")
        prev_content[-1]['Winner'] = 'LLM 2'
    else:
        st.info("It's a tie!")
        prev_content[-1]['Winner'] = 'NA'

    if show_credits:
        st.sidebar.write(f"Credit Balance: ${chatbot1._get_credits():.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Next Round", key=f"next{round_number}")

    with col2:
        st.button("New Chat", key=f"new_chat", on_click=st.session_state['new_chat_cb'])
