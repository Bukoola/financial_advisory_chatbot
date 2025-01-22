import os
import json
import openai
import streamlit as st
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
nltk.download('wordnet')

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["api"]["token"]

# Define the directory where processed data is stored
data_folder = "output_files"

# Function to load processed data
def load_data(data_folder):
    data = {}
    if not os.path.exists(data_folder):
        st.error(f"The folder '{data_folder}' does not exist.")
        return data

    for file_name in os.listdir(data_folder):
        if file_name.endswith('_normalized.txt'):  # Use normalized text
            file_path = os.path.join(data_folder, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data[file_name.replace('_normalized.txt', '')] = file.read()
            except Exception as e:
                st.error(f"Error reading file {file_name}: {e}")
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

# Main Streamlit app
def main():
    st.title("AI Assistant for Financial and Legal Topics")

    # Load the processed data
    st.write("Loading data...")
    data = load_data(data_folder)
    st.write(f"Loaded {len(data)} documents.")

    # User input for question
    question = st.text_input("Ask a question:", placeholder="Type your question here...")

    # User input for optional document name
    document_name = st.text_input("Specify a document (optional):", placeholder="Leave blank to use all documents")
    
    if st.button("Submit"):
        if not question:
            st.error("Please enter a question.")
        else:
            st.write("Querying GPT-4...")
            answer = query_gpt4(data, question, document_name if document_name else None)
            if answer:
                st.subheader("Answer:")
                st.write(answer)

# Run the Streamlit app
if __name__ == "__main__":
    main()
