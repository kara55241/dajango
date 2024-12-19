import openai
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()

def get_chatgpt_response(question):
    try:
        chat_prompt = ChatPromptTemplate.from_messages(
            [
            ("system", "You are an AI expert providing information about Neo4j and Knowledge Graphs."),
            ("human", "{input}"),
            ]
        )
        llm = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            model_name="gpt-4o-mini"
            
        )
        llm_chain=chat_prompt | llm
        response =llm_chain.invoke(question)
        return response.content
    except openai.error.OpenAIError as e:
        print(f"OpenAI API 發生錯誤：{e}")
        return "抱歉，我無法生成回應。"