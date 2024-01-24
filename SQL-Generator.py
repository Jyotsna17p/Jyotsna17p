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
    st.title("SQL Generator via User Input Text or File Upload")

    #Input Box
    input_text =  st.text_area("Type your text")
    #Divider
    st.divider()
    # File Upload Option
    uploaded_file = st.file_uploader("Choose only text file")
    if uploaded_file is not None and uploaded_file.type == "text/plain":
            # For plain text files
            text_contents = uploaded_file.read().decode("utf-8")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write(get_sql_query(text_contents))

    if input_text is not None and st.button("Generate SQL"):
        st.write(get_sql_query(input_text))
        
    
if __name__ == "__main__":
    main()
