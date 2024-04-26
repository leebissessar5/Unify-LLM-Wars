import streamlit as st

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
            credits = chatbot1.get_credits()
            st.sidebar.write(f"Credit Balance: ${credits}")

        if not st.button("Next Round", key=f"next{round_number}"):
            break

        round_number += 1
        prompt = "Generate another random question."