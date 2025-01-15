import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app title
st.title("Chatbot on Streamlit")

# Sidebar instructions
st.sidebar.title("About")
st.sidebar.info("This is a chatbot powered by OpenAI GPT, deployed on Streamlit.")

# Initialize session state for storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful financial assistant."}
    ]

# Display chat messages from history on app rerun
for msg in st.session_state.messages[1:]:  # Skip the system message
    role = "You" if msg["role"] == "user" else "Bot"
    st.write(f"**{role}:** {msg['content']}")

# Input field for user input
user_input = st.text_input("You:")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get the assistant's response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=st.session_state.messages
        )
        reply = response["choices"][0]["message"]
        st.session_state.messages.append(reply)

        # Display assistant response
        st.write(f"**Bot:** {reply['content']}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
