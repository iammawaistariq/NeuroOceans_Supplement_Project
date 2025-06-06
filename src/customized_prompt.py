from src.pubmed_article import fetch_pubmed_articles

def generate_customized_prompt(user_profile, user_query="Generate response based on medical data"):

    print("2. Generate Customzied Prompt function")

    def filter_data(data):
        if isinstance(data, dict):
            return {k: filter_data(v) for k, v in data.items() if v not in (None, {}, [], ())}
        elif isinstance(data, list):
            return [filter_data(v) for v in data if v not in (None, {}, [], ())]
        return data

    filtered_profile = filter_data(user_profile)

    pubmed_data_article_details = fetch_pubmed_articles(user_data=user_profile, user_input=user_query, max_results=3)

    print("Pubmed Data fetched Successfully")

    # Return the customized prompt
    customized_prompt = f"""

    User Profile: {filtered_profile}

    User Query: {user_query}

    Relevant PubMed Research Articles:
    {pubmed_data_article_details}
    """
    return customized_prompt
