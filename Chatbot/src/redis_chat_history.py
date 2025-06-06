import redis
from typing import Dict, Any
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ Redis connection setup
REDIS_URL = os.getenv("REDIS_URL")

def validate_redis_connection():
    try:
        client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)
        client.ping()  # Ping Redis to check connectivity
        print("✅ Connected to Redis successfully.")
        return client
    except redis.exceptions.AuthenticationError:
        return "❌ Redis authentication failed. Check your credentials."
    except Exception as e:
        return f"❌ Redis connection error: {e}"

# ✅ Initialize Redis client
redis_client = validate_redis_connection()

def save_user_data(user_id: str, user_data: dict):
    """
    Stores user data separately in Redis.
    """
    key = f"user_data:{user_id}"
    redis_client.set(key, str(user_data))  # Convert to string before storing

def get_stored_user_data(user_id: str) -> str:
    """
    Retrieves user data from Redis.
    """
    key = f"user_data:{user_id}"
    user_data = redis_client.get(key)
    return user_data if user_data else None  # Return None if no data found

def get_chat_history(user_id: str) -> RedisChatMessageHistory:
    """
    Retrieves a Redis-backed chat history for the given user_id.
    Returns only the last 10 messages.
    """
    return RedisChatMessageHistory(session_id=str(user_id), url=REDIS_URL)

def clear_chat_history(user_id: str) -> Dict[str, str]:
    """
    Clears the chat history for a given user_id.
    """
    chat_history = get_chat_history(user_id)
    chat_history.clear()
    return {"message": f"Chat history cleared successfully for user ID {user_id}"}

def get_user_chat_history(user_id: str) -> Dict[str, Any]:
    """
    Retrieves the chat history for a user.
    """
    chat_history = get_chat_history(user_id)
    return {
        "chat_history": [
            {"role": msg.type, "content": msg.content}
            for msg in chat_history.messages
        ]
    }
