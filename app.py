import os
import openai
import streamlit as st

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["api"]["token"]

# Define the directory where processed data is stored
data_folder = "output_files"

# Function to load processed data
def load_data(data_folder):
    data = {}
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)  # Create the directory if it doesn't exist
        st.warning(f"Directory '{data_folder}' not found. Created an empty directory.")
        return data

    for file_name in os.listdir(data_folder):
        if file_name.endswith('_normalized.txt'):  # Use normalized text
            file_path = os.path.join(data_folder, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                data[file_name.replace('_normalized.txt', '')] = file.read()
    return data

# Function to create a GPT-4 query
def query_gpt4(data, question, document_name=None):
    context = ""
    if document_name:
        context = data.get(document_name, "Document not found.")
    else:
        context = "\n\n".join(data.values())  # Use all documents if none specified

    # GPT-4 prompt
    prompt = (
        "You are an AI assistant trained on financial and legal topics.\n"
        "Use the following context to answer the question:\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # Lower temperature for factual accuracy
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"Error calling GPT-4 API: {e}")
        return None

# Main function to interact with the system
def main():
    st.title("Financial Advisory Chatbot")
    st.write("Ask questions about financial or legal topics.")

    # Load the processed data
    st.write("Loading data...")
    data = load_data(data_folder)
    st.write(f"Loaded {len(data)} documents.")

    # Get user input
    question = st.text_input("Enter your question:")
    document_name = st.text_input("Enter the document name (optional):")

    if st.button("Get Answer"):
        if question.strip():
            st.write("Querying GPT-4...")
            answer = query_gpt4(data, question, document_name or None)
            st.write("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")

# Run the program
if __name__ == "__main__":
    main()
