from src.customized_prompt import generate_customized_prompt
from src.process_LLM_response import process_llm_response
from src.supplement_recommender_LLM import supplement_recommending_LLM
from src.preprocessing_user_data import preprocess_medical_data
import sys
import os
from fastapi import FastAPI

from Test_Report.src.extract_report_content import read_report
from pydantic import BaseModel, Field
from typing import List, Optional
from Chatbot.src.redis_chat_history import get_user_chat_history, clear_chat_history, save_user_data
from Chatbot.src.chat_handler import run_chat_chain
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()
pubmed_api_key = os.getenv("pubmed_api_key")
openai_api_key = os.getenv("OPENAI_API_KEY")
Tavily_API_key = os.getenv("Tavily_API_key")

# Add the 'src' folder to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Initialize FastAPI app
app = FastAPI()

###################################################################################################################

class UserProfile(BaseModel):
    # Personal Info
    age: Optional[int] = None
    gender: Optional[str] = None
    
    # Height in inches (calculated from feet and inches in preprocessing)
    height_in_feet: Optional[int] = None  # Height in inches
    height_in_inches: Optional[int] = None  # Height in inches
    
    # Weight in lbs (as per the preprocessing function)
    weight: Optional[float] = None  # Weight in lbs
    
    # Activity level (e.g., 'Moderate', 'Active')
    activity_level: Optional[str] = None
    
    # Medical conditions and allergies, represented as lists
    medical_conditions: List[str] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)

    # current_medical_conditions: Optional[str] = None
    current_medications: List[str] = Field(default_factory=list)
    supplement_plan: List[dict] = Field(default_factory=list)
    diet_restriction:Optional[str] = None
    smoking_status:Optional[str] = None
    alcohol_consumption: Optional[str] = None
    monthly_budget: Optional[str] = None

    # Test Reports
    blood_work_test:Optional[dict]=None
    genetic_test:Optional[dict]=None

    average_sleep:Optional[float]=0.0
    concerns:Optional[str]=None

    # Health goals (split from string as list)
    health_goals: List[dict] = Field(default_factory=list)

    user_query: Optional[str] = "Generate a supplement plan based on user data, health goals, and medical reports"

@app.post("/")
async def main(user_profile: UserProfile):

    user_profile_data = user_profile.dict()

    user_query = user_profile_data.pop("user_query")

    # Pre-process data to remove unwanted data
    processed_user_profile = preprocess_medical_data(user_profile_data)

    # Generate customized prompt with PubMed research
    customized_prompt = generate_customized_prompt(
        processed_user_profile, user_query=user_query
    )

    # Generate LLM response
    llm_response = supplement_recommending_LLM(customized_prompt)

    generated_supplement_plan = process_llm_response(llm_response)

    return {"supplement_plan": generated_supplement_plan}

###################################################################################################################

class ChatbotAPI(BaseModel):
    user_id: str
    user_query: str

@app.post("/chat")
async def chat_endpoint(request: ChatbotAPI):
    """
    The API endpoint for interacting with the chatbot. 
    Takes in user_id and user_query, invokes the chatbot and returns the response.
    """
    response = run_chat_chain({"input": request.user_query, "user_id": request.user_id})
    return response

######################################################################################################################



# ✅ Request model for updating user data
class UserData(BaseModel):
    user_id: str
    user_data: dict

@app.post("/update_user_data/")
async def update_user_data(user_data: UserData):
    """
    API to update user data in Redis.
    """
    try:
        save_user_data(user_data.user_id, user_data.user_data)
        return {"message": f"User data updated successfully for user ID {user_data.user_id}"}
    except Exception as e:
        return {"error": "Failed to update user data", "details": str(e)}
    
###################################################################################################################

@app.get("/get_user_data/{user_id}")
async def fetch_user_data(user_id: str):
    """
    API to fetch stored user data from Redis.
    """
    stored_data = get_user_chat_history(user_id)
    if stored_data is None:
        return {"user_id": user_id, "user_data": "User-ID not found"}
    return {"user_id": user_id, "user_data": stored_data}

######################################################################################################################

@app.delete("/clear-chat-history/{user_id}")
async def clear_chat_history_endpoint(user_id: str):
    """
    Endpoint to clear chat history for a given user.
    """
    result = clear_chat_history(user_id)
    return result

########################################################################################################

class Read_Test_Report(BaseModel):
    url: str  # URL for the test report file

@app.post("/read_test_report") 
async def read_test_report(request: Read_Test_Report):

    return read_report(request.url)

########################################################################################################
