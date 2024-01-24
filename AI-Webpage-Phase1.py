import openai
import chromadb
import os
import requests
from bs4 import BeautifulSoup

import streamlit as st
os.environ["TOKENIZERS_PARALLELISM"] = "false"
client = openai.OpenAI(api_key="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")

documents = []
metadatas = []
ids = []

webpage_test_collection = chromadb.Client().get_or_create_collection("webpage_test1_database")

def read_files_from_folder(folder_path):
    file_data = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith("Webpage_Data.txt"):
            with open(os.path.join(folder_path, file_name), 'r') as file:
                content = file.read()
                file_data.append({"file_name": file_name, "content": content})
            
    return file_data

def store_data_to_chroma_db(file_data):
    for index, data in enumerate(file_data):
        webpage_test_collection.add(
            documents=data['content'],
            metadatas={'source': data['file_name']},
            ids=f"id{(index + 1)}"
        )

def get_nearest_vector_for_query(query_text):

    result = webpage_test_collection.query(
                query_texts=[query_text],
                n_results=3,
                include=["metadatas", "embeddings","documents","distances"]
                )
    return result.get('documents')

def get_answer(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

def extract_data_from_url(content):
    page = requests.get(content)
    soup = BeautifulSoup(page.content, "html.parser")
    data = soup.get_text()
    modified_data = data.splitlines()
    final_data = list(filter(bool, modified_data))
    return final_data

def write_text_data_to_file(data, folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    with open(f"{folder_name}/Webpage_Data.txt",'w') as output :
        output.writelines(data)

def main():
    st.title("AI-Powered Webpage - Phase I")

    input_url =  st.text_input("Enter the url")
    options = st.radio(
        "Action to be done with above URL",
        ["None", "Summarize", "Ask Question"])
    
    final_data = ""
    if options == 'Ask Question' :
            query_input = st.text_input("Enter you query ")
            ask_quest = st.button("ASK")

    if input_url is not None  and options == 'Summarize' and input_url is not None :
        
        final_data = extract_data_from_url(input_url)
        prompt = f"""You are an AI helper who is trained to summarize  
        below context in simple and lame language
        Context :
        ```{final_data}```
        """
        st.write(get_answer(prompt))

    if input_url is not None  and options == 'Ask Question' and query_input is not None and ask_quest:
            
            final_data = extract_data_from_url(input_url)
            write_text_data_to_file(final_data,"GENAI-PYTHON")
            file_data = read_files_from_folder("GENAI-PYTHON")
            store_data_to_chroma_db(file_data)
            get_nearest_vector_for_query(query_input)

            prompt1 = f"""You are an assistant trained to answer questions using the given context.
                    Context :
                    ```{final_data}```,
                    Ensure your responses are well-supported with relevant information from the article
                    ```{query_input}```
                    If you don't find any relevant data give this response
                    Example : No relevant data 
                    """
            st.write(get_answer(prompt1))    

if __name__ == "__main__":
    main()
