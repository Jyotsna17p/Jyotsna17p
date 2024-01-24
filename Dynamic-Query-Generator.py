import streamlit as st
import openai

client = openai.OpenAI(api_key="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")

def get_sql_query(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def main():
    st.title("Query Generator")

    selected_database =  st.radio(options=["MySQL"],label="Select your database")
    table_name = st.text_input("Table Name")
    column_name = st.text_input("Column Name (Comma seperated)")
    text_to_convert = st.text_area("Text Query")

    convert_button = st.button("Generate Query")

    prompt = f"""\n
    Language {selected_database} \n
    Table {table_name}, columns = [{column_name}] \n
    {selected_database} query for {text_to_convert} ?\n
    """
    if table_name is not None and column_name is not None and text_to_convert is not None and convert_button:
        st.write("Prompt :" + prompt + "\n")
        st.write(get_sql_query(prompt))
        

if __name__ == "__main__":
    main()
