import openai
import streamlit as st

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app title with style
st.markdown(
    """
    <div style="background-color:#4CAF50;padding:10px;border-radius:5px;">
        <h1 style="color:white;text-align:center;">Financial Advisory Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar instructions with style
st.sidebar.markdown(
    """
    <div style="background-color:#2196F3;padding:10px;border-radius:5px;">
        <h3 style="color:white;text-align:center;">About</h3>
        <p style="color:white;text-align:center;">
            This is a chatbot powered by OpenAI GPT, deployed on Streamlit.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input field for user input with a placeholder
st.markdown("### What would you like to know? :")
user_input = st.text_input("", placeholder="Ask me anything...", key="user_input")

# Add a button to process user input
if st.button("Send"):
    if user_input:
        # Append user message to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Get GPT-4 response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=st.session_state["messages"]
        )
        
        reply = response["choices"][0]["message"]["content"]
        st.session_state["messages"].append({"role": "assistant", "content": reply})

# Display chat history with alternating colors
st.markdown("### Chat History:")
for idx, msg in enumerate(st.session_state["messages"]):
    role = "You" if msg["role"] == "user" else "Bot"
    color = "#f0f0f0" if idx % 2 == 0 else "#e8e8e8"
    st.markdown(
        f"""
        <div style="background-color:{color};padding:10px;border-radius:5px;margin:5px 0;">
            <strong>{role}:</strong> {msg['content']}
        </div>
        """,
        unsafe_allow_html=True,
    )