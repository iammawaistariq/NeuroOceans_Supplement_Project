from Chatbot.utils.config import User_Data_Access_API, DJANGO_SERVICE_API_KEY
import requests

def get_user_data(user_id):
    try:
        api_url = f"{User_Data_Access_API}{user_id}/"

        headers = {
            "DJANGO_SERVICE_API_KEY": DJANGO_SERVICE_API_KEY
        }

        response = requests.get(api_url, headers=headers)
        # print("Request Response =", response)

        requested_user_data = response.json()
        # print("user Data = ", requested_user_data)

        return requested_user_data

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
