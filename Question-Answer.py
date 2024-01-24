import streamlit as st
import openai

client = openai.OpenAI(api_key="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")

def get_data(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


def main():
    st.title("Question-Answer System (Fine Tunning)")

    #Input Box
    input_text =  st.text_area("Type your input context")
    
    quest_text =  st.text_area("Ask questions based on above data")
    #Divider
    st.divider()
    prompt = f"""You are an assistant trained to answer questions using the given context.
    Context :
    ```{input_text}```,
    Ensure your responses are well-supported with relevant information from the article
    ```{quest_text}```
    """

    if input_text is not None  and quest_text is not None and st.button("Get Answer"):
        st.write(get_data(prompt))
        
    




if __name__ == "__main__":
    main()
