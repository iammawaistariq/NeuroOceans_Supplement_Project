def preprocess_medical_data(data):

    print("1. Processing Medica Data function")
    try:
        # Filter out keys with non-empty values
        processed_data = {
            key: value
            for key, value in data.items()
            if value not in (None, "", [], {})  # Skip None, empty strings, lists, or dictionaries
        }

        print("porcessed data",processed_data)
        return processed_data
        
    except AttributeError:
        # Handle case where data is not a dictionary
        return {}
    except Exception as e:
        # Log any other unexpected errors
        print(f"Error preprocessing medical data: {str(e)}")
        return {}