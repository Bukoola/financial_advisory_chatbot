import os
import json
import openai
import streamlit as st
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import nltk

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["api"]["token"]

# Define the directory where processed data is stored
data_folder = "output_files"

# Function to load processed data
def load_data(data_folder):
    data = {}
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
        print(f"Error calling GPT-4 API: {e}")
        return None

# Main function to interact with the system
def main():
    # Load the processed data
    print("Loading data...")
    data = load_data(data_folder)
    print(f"Loaded {len(data)} documents.")

    while True:
        # Get user input
        print("\nAsk a question or type 'exit' to quit.")
        question = input("Question: ").strip()
        if question.lower() == 'exit':
            break

        # Optional: Specify a document
        print("Enter the document name (or press Enter to search all):")
        document_name = input("Document Name: ").strip()
        if not document_name:
            document_name = None

        # Query GPT-4
        print("Querying GPT-4...")
        answer = query_gpt4(data, question, document_name)
        print("\nAnswer:")
        print(answer)

# Run the program
if __name__ == "__main__":
    main()
