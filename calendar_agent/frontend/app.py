import streamlit as st
import requests

st.set_page_config(page_title="AI Appointment Booking Assistant 🤖📅")
st.title("AI Appointment Booking Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Type here to talk to the bot...")

if user_input:
    st.session_state.history.append(("You", user_input))
    with st.spinner("Bot is thinking..."):
        try:
            response = requests.post("http://localhost:8000/chat", json={"message": user_input})

            # Check if backend responded with valid JSON
            if response.status_code == 200:
                json_data = response.json()
                bot_msg = json_data.get("response", "No response from server.")
            else:
                bot_msg = f"Backend error: {response.status_code}"

        except requests.exceptions.RequestException as e:
            bot_msg = f"Connection error: {e}"
        except Exception as e:
            bot_msg = f"Unexpected error: {e}"

    st.session_state.history.append(("Bot", bot_msg))

# Show full chat history
for sender, msg in st.session_state.history:
    st.markdown(f"**{sender}:** {msg}")
