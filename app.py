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
    st.session_state["messages"] = []

# Input field for user input
user_input = st.text_input("You:", "")

if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    
    # Get GPT-4 response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=st.session_state["messages"]
    )
    
    reply = response["choices"][0]["message"]["content"]
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    
    # Display chat history
    for msg in st.session_state["messages"]:
        role = "You" if msg["role"] == "user" else "Bot"
        st.write(f"**{role}:** {msg['content']}")