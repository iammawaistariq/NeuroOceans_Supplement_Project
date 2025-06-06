from openai import OpenAI
from utils.config import openai_api_key
from typing import List
from pydantic import BaseModel, Field
from utils.config import front_end_supplement_prompt


# Define the data models with required fields
class MedicalGradeSupplement(BaseModel):
    product_name_and_brand: str
    dosage_and_instructions: str

class Supplement(BaseModel):
    supplement_name: str
    supplement_benefits: str
    medical_grade_supplements: MedicalGradeSupplement

class SupplementsResponse(BaseModel):
    supplements: List[Supplement] = Field(..., description="List of supplements")

# Initializing LLM
def supplement_recommending_LLM(user_data_and_query):

    print("3. Supplement recommending LLM")
    try:
        # OpenAI client setup
        client = OpenAI(api_key=openai_api_key)

        # Simulate user query and LLM interaction
        messages = [
            {"role":"system","content": front_end_supplement_prompt},
            {"role": "user", "content": user_data_and_query},
        ]

        # Perform function call
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            response_format=SupplementsResponse,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        # Handle errors and provide feedback
        print(f"Error occurred: {e}")
        return "An error occurred while processing your request. Please try again later."
