import pandas as pd
import requests
from io import StringIO

def csv_content_extracting(csv_url):
    """Extract and clean text data from a CSV file using pandas."""
    try:
        # Step 1: Download CSV file
        response = requests.get(csv_url)
        response.raise_for_status()  # Ensure the request was successful
        
        # Validate content type (optional but recommended)
        if 'text/csv' not in response.headers.get('Content-Type', ''):
            raise ValueError("The URL did not return a valid CSV file.")

        # Step 2: Read CSV into Pandas DataFrame
        csv_text = response.content.decode('utf-8')
        df = pd.read_csv(StringIO(csv_text))

        # Step 3: Clean the DataFrame
        df = df.fillna("")  # Replace NaN with empty strings
        df = df.astype(str)  # Ensure all data is string format

        # Step 4: Convert DataFrame to a structured text format
        structured_text = df.to_csv(index=False, sep=",", lineterminator="\n")

        return structured_text.strip()

    except Exception as e:
        return f"Error processing CSV: {e}"
