import openai
import chromadb
import os
import pandas
os.environ["TOKENIZERS_PARALLELISM"] = "false"
client = openai.OpenAI(api_key="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")

documents = []
metadatas = []
ids = []

cyptocurrency_collection = chromadb.Client().get_or_create_collection("cyptocurrency_test_database")

def read_files_from_folder(folder_path):

    with open('cryptocurrency.txt', 'r') as file:
        content = file.read()
    sections = content.split('\n\n')

    crypto_data = []

    for section in sections:
        parts = [part.strip() for part in section.split(':')]
        crypto_data.append(parts)

    for data in crypto_data:
        documents.append(data[1])
        metadatas.append({'source': data[0]})
        ids.append(data[0])
        cyptocurrency_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
folder_path = "GENAI-PYTHON"
file_data = read_files_from_folder(folder_path) 
def get_query_result_vector(query_text):
    result = cyptocurrency_collection.query(
                query_texts=[query_text],
                n_results=10,
                include=["metadatas", "embeddings","documents","distances"]
                )
    return result.get('documents')

def get_sql_query(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

print("Hey I am you AI chat bot ! Post your query ! Type 0 to exit")
while True:
    query_input = input("Jyotsna : ")
    if query_input == "0":
        print("Thanks for using me")
        break
    else:
        prompt = f"""You are an assistant trained to answer questions using the given context.
                Context :
                ```{get_query_result_vector(query_input)}```,
                Ensure your responses are well-supported with relevant information from the article
                ```{query_input}```
                If you don't find any relevant data give this response
                Example : No relevant data 
                """
    print("AI Bot : " +  get_sql_query(prompt))
