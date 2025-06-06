import fitz  # PyMuPDF
import requests
from io import BytesIO

def pdf_content_extracting(pdf_url):
    """Download PDF from an S3 URL and extract all text content."""
    try:
        # Step 1: Download the PDF file
        response = requests.get(pdf_url)

        response.raise_for_status()  # Ensure the request was successful

        # Check if the response is indeed a PDF
        content_type = response.headers.get('Content-Type')
        if 'application/pdf' not in content_type:
            raise ValueError(f"The URL did not return a PDF. Content-Type: {content_type}")
        
        # Step 2: Open the PDF from the byte stream
        doc = fitz.open(stream=BytesIO(response.content), filetype="pdf")

        # Step 3: Extract text from each page
        full_text = []
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")  # Extract text
            full_text.append(text.strip())  # Remove unnecessary spaces
        
        # Return the combined text content from all pages
        combined_text = "\n".join(full_text).strip()

        if not combined_text:
            return "No text found in the PDF."
        
        return combined_text

    except requests.exceptions.RequestException as e:
        return f"Failed to download the PDF: {e}"
    except ValueError as ve:
        return f"Value Error: {ve}"
    except Exception as e:
        return f"An error occurred while processing the PDF: {e}"
