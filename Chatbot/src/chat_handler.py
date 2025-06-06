from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from Chatbot.src.user_data import get_user_data
from Chatbot.utils.config import system_prompt, OPENAI_API_KEY
from Chatbot.src.redis_chat_history import (
    get_stored_user_data, save_user_data, get_chat_history
)

# ✅ Initialize OpenAI chat model
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    max_tokens=2000,
    api_key=OPENAI_API_KEY
)

def _initialize_chain() -> Any:
    """
    Creates the prompt template and chains it with the model.
    Includes user data inside the system message.
    """
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="message_history"),
        ("human", "{input}")  # ✅ User input
    ])
    
    return prompt | model

def run_chat_chain(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the user's query, retrieves and updates Redis chat history, 
    and invokes the chat pipeline while keeping user data separate.
    """
    user_query = inputs["input"]
    user_id = inputs.get("user_id")

    # ✅ Retrieve stored user data or fetch it if not found
    stored_user_data = get_stored_user_data(user_id)

    if stored_user_data is None:
        fetched_user_data = get_user_data(user_id)
        save_user_data(user_id, fetched_user_data)
        stored_user_data = fetched_user_data  # Use the newly fetched data


    # ✅ Get Redis chat history (last 10 messages)
    chat_history = get_chat_history(user_id)
    limited_chat_history = chat_history.messages[-10:]

    # ✅ Initialize the chat pipeline with user data
    chain_pipeline = _initialize_chain()

    # ✅ Build chain inputs
    chain_inputs = {
        "input": user_query,
        "message_history": [HumanMessage(content=f"User Data: {stored_user_data}")] + limited_chat_history
    }

    # ✅ Invoke the chat pipeline
    response = chain_pipeline.invoke(chain_inputs)
    generated_response = response.content

    # ✅ Store the conversation in Redis (limit to last 10 messages)
    chat_history.add_message(HumanMessage(content=user_query))
    chat_history.add_message(AIMessage(content=generated_response))

    return {"response": generated_response}
