# LLM-Wars

## Introduction
### Overview
**LLM Wars** is a web application built with Streamlit that sets up a dynamic competition between two Large Language Models (LLMs). The LLMs engage in a structured debate where they challenge each other by generating complex prompts, responding to those prompts, and evaluating the responses. This application demonstrates the natural language capabilities of modern AI models in an interactive competitive environment with visualizations.

### Objective
The main goal of LLM Wars is to provide a creative and educational platform for testing AI models against each other following predefined rules. It highlights the strengths and limitations of language models while presenting AI capabilities engagingly to users.

### Tech Stack
- **Streamlit**: Used for creating the web application interface that is intuitive and interactive.
- **Unify AI**: Provides the backend LLMs that power the interactions within the application. Unify's API is utilized to send prompts to the LLMs and receive their responses in real-time.

### Application Flow
1. **Initialization**: Users start by selecting two competing LLMs and one judge LLM from a predefined list of available models.
2. **Competition Cycle**:
   - **Prompt Suggestion**: LLM1 generates a challenging prompt.
   - **Response Generation**: LLM2 attempts to respond accurately to the prompt.
   - **Verification**: LLM1 verifies the correctness of LLM2's response.
   - **Judgment**: The judge LLM evaluates the interaction. If LLM2's response is deemed incorrect, LLM1 is declared the winner, and the cycle ends. Otherwise, roles are reversed, and the cycle repeats with LLM2 generating the next prompt.
3. **Visualization**: The application provides a visual representation of the ongoing interaction, scores, and decisions made by the judge LLM.

### Motivation
LLM Wars demonstrates novel LLM applications beyond common use cases by creating a competitive AI environment. This pushes the boundaries of what language models can creatively and adaptively achieve. It also serves an educational purpose demystifying AI for audiences like students and professionals.

### Key Concepts
- **Natural Language Understanding and Generation**: At the core of LLM Wars is the ability of LLMs to understand and generate human-like text, showcasing advancements in AI language models.
- **API Integration**: Demonstrates how to effectively integrate and utilize third-party APIs (Unify AI) within a Python-based application.

## Quick Demo
https://github.com/leebissessar5/Unify-LLM-Wars/assets/120032434/0a6f60c0-e679-4577-b409-9d5d6df11c9c

## Repository and Deployment
The source repository for this project can be found [here](https://github.com/leebissessar5/Unify-LLM-Wars).

To get started quickly, you can run the app hosted on [Streamlit](https://unify-llm-wars-tftznesvztdt2bwsqgub3r.streamlit.app/).

### Running the Application Locally
Open a terminal located in this directory and first install all the dependencies with `pip install`:

```bash
pip install -r requirements.txt
```

And you're done! Simply launch the app with:
```bash
streamlit run main.py
```


## Contributors
| Name | GitHub Profile |
|------|----------------|
| Lee Bissessar | [leebissessar](https://github.com/leebissessar5) |
| Glorry Sibomana | [WHITELOTUS0](https://github.com/WHITELOTUS0) |
| Kato Steven Mubiru | [KatoStevenMubiru](https://github.com/KatoStevenMubiru) |
