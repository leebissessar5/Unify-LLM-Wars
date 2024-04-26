import streamlit as st

def llm_battle(chatbot1, chatbot2, judge, show_credits):
    prompt = "Generate a random question that you need to get answered, without giving an answer yourself."
    round_number = 1

    chatbots = (chatbot1, chatbot2) if round_number % 2 == 1 else (chatbot2, chatbot1)
    first_player, second_player = ('LLM 1', 'LLM 2') if round_number % 2 == 1 else ('LLM 2', 'LLM 1')

    st.markdown(f"*Round {round_number}*, First player's turn: {'LLM 1' if round_number % 2 == 1 else 'LLM 2'}")

    with st.chat_message("1"):
        player1_question = st.write_stream(chatbots[0]._process_input(prompt, show_credits=False, show_provider=False))

    with st.chat_message("2"):
        player2_answer = st.write_stream(chatbots[1]._process_input(player1_question, show_credits=False, show_provider=False))
    
    with st.chat_message("1"):
        player1_evaluation = st.write_stream(chatbots[0]._process_input(f"Evaluating {second_player}'s answer: {player2_answer}", show_credits=False, show_provider=False))

    with st.chat_message('Judge'):
        judge_evaluation = st.write_stream(
            judge._process_input(f'''Judge the responses: {first_player}'s Question: {player1_question}\n
            {second_player}'s Answer: {player2_answer}\n
            {first_player}'s Evaluation of {second_player}: {player1_evaluation}\n
            After judging, state in the final line who is the winner, *exactly* like this: **Winner: LLM 1**''', 
            show_credits=False, show_provider=False)
        )

    if "Winner: LLM 1" in judge_evaluation:
        st.success("LLM 1 wins!")
    elif "Winner: LLM 2" in judge_evaluation:
        st.success("LLM 2 wins!")
    else:
        st.info("It's a tie!")

    if show_credits:
        st.sidebar.write(f"Credit Balance: ${chatbot1._get_credits():.2f}")

    # if st.button("Next Round", key=f"next{round_number}"):
    #     pass

    round_number += 1
    prompt = "Generate another random question."