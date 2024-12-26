import uuid

import streamlit as st
import requests
import time


API_ENDPOINT = "http://127.0.0.1:8000/"

# --------------- Streamlit Support Functions -----------------#

# Function to stream response
def stream_response(response_text: str):
    for word in response_text.split(" "):
        yield word + " "
        time.sleep(0.03)

# Function to load css file for custom styling
def local_css(filename: str) -> None:
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def clear_chat():
    st.session_state["messages"] = []

def new_chat():
    del st.session_state["session_id"]
    st.session_state["messages"] = []

local_css("./assets/css/styles.css")

#------------------ Streamlit Start Here --------------------#


if "session_id" not in st.session_state:
    st.session_state["session_id"] = requests.get(url=f"{API_ENDPOINT}/get_session_id").json()["session_id"]

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
             "role": "assistant",
             "content": "I'm your basic chatbot. Ask me anything!"
            }
        ]


with st.sidebar:
    st.title("Your Session ID:")
    st.write(st.session_state["session_id"])

# Handle new message
prompt = st.chat_input("Type your question here")

st.button("Clear Chat", key="clear_chat", on_click=clear_chat, icon=":material/cancel:")
st.button("New Chat", key="new_chat", on_click=new_chat, icon=":material/add_circle:")

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    # Add user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get AI response
    with st.spinner("AI Thinking..."):
        api_response = requests.post(
            url=f"{API_ENDPOINT}/chatbot_response/",
            json={
                "prompt": prompt,
                "session_id": st.session_state["session_id"]
            }
        )

    # Refresh the conversation display
    if api_response.status_code == 200:
        ai_response = api_response.json()["response"]

        # Stream the new assistant response
        with st.chat_message("assistant"):
            st.write_stream(stream_response(ai_response))
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

    else:
        st.error("Failed to get response from the AI Service")



