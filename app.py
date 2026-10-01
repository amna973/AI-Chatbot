import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")


# ---------------------------------------------------------
# Check API key
# ---------------------------------------------------------

if not api_key:
    st.error(
        "OpenRouter API key is missing. "
        "Please add OPENROUTER_API_KEY to your .env file."
    )
    st.stop()


# ---------------------------------------------------------
# OpenRouter client
# ---------------------------------------------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful AI assistant.

Your job is to:
- Answer the user's questions clearly.
- Use simple language when appropriate.
- Be accurate and useful.
- Be polite and professional.
- Organize longer answers with headings or bullet points.
"""


# ---------------------------------------------------------
# Initialize conversation history
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 I'm your AI assistant. "
                "How can I help you today?"
            )
        }
    ]


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("🤖 AI Chatbot")

st.caption("Powered by OpenRouter Free Models")


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:

    st.header("Chat Settings")

    st.write(
        "Your conversation is stored temporarily "
        "during this browser session."
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Chat cleared. "
                    "How can I help you?"
                )
            }
        ]

        st.rerun()


# ---------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ---------------------------------------------------------
# Chat input
# ---------------------------------------------------------

prompt = st.chat_input(
    "Type your message here..."
)


# ---------------------------------------------------------
# Send message to OpenRouter
# ---------------------------------------------------------

if prompt:

    # Add user's message to history
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user's message
    with st.chat_message("user"):

        st.markdown(prompt)


    # Prepare messages for the API
    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    api_messages.extend(
        st.session_state.messages
    )


    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=api_messages,
                    stream=False,
                    max_tokens=1000
                )

                ai_response = (
                    response.choices[0]
                    .message
                    .content
                )


                # Display response
                st.markdown(ai_response)


                # Save response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )


            except Exception as error:

                print(
                    "OpenRouter API error:",
                    str(error)
                )

                st.error(
                    "Sorry, I couldn't get a response "
                    "from the AI. Please try again."
                )