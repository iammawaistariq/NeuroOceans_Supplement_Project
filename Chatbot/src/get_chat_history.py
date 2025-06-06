from Chatbot.utils.config import DJANGO_SERVICE_API_KEY
import requests

def API_get_user_chat_history(user_id):
    try:
        api_url = f"https://3-104-203-150.nip.io/api/v1/assistant/chat-history/{user_id}/"

        headers = {
            "DJANGO_SERVICE_API_KEY": DJANGO_SERVICE_API_KEY
        }

        response = requests.get(api_url, headers=headers)
        # print("Request Response =", response)

        requested_user_data = response.json()
        # print("user Data = ", requested_user_data)

        # print("Checking Chat history API",requested_user_data.keys())

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
