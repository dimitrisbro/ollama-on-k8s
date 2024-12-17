import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
import os


st.set_page_config(page_title="Simplr LLM",
    page_icon="👋",
    layout="wide")
st.title("This is you personal assistant 💬")
      
ollama_url = os.environ.get("OLLAMA_URL", "http://localhost")
ollama_port = os.environ.get("OLLAMA_PORT", "11434")
new_url = ollama_url+":"+ollama_port
print(new_url)
# Define Model
llm = OllamaLLM(model="mistral", base_url=new_url, verbose=True)

# to-do parse outputs
def my_parser(outputs):
    print(outputs)
    return outputs

# Chat bot
msgs = StreamlitChatMessageHistory(key="langchain_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

# Set up the LangChain, passing in Message History
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI chatbot having a conversation with a human. Be sort and concise"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | llm

# to-do: bebug error in chat history causing Error in RootListenersTracer.on_chain_end callback: ValueError()
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
) 

full_chain = chain_with_history | my_parser

# Render current messages from StreamlitChatMessageHistory
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# If user inputs a new prompt, generate and draw a new response
if prompt := st.chat_input():
    st.chat_message("human").write(prompt)
    # Note: new messages are saved to history automatically by Langchain during run
    config = {"configurable": {"session_id": "any"}}
    response = full_chain.invoke({"question": prompt}, config)
    st.chat_message("ai").write(response)
