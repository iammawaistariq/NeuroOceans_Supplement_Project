import requests

def txt_content_extracting(txt_url):
    """Extract text from a TXT file."""
    try:
        response = requests.get(txt_url)
        response.raise_for_status()

        if 'text/plain' not in response.headers.get('Content-Type', ''):
            raise ValueError("The URL did not return a valid TXT file.")

        return response.text.strip() or "No content found in the TXT file."

    except Exception as e:
        return f"Error processing TXT file: {e}"
