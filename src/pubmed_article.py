import requests
import time
from xml.etree import ElementTree
from openai import OpenAI
from utils.config import pubmed_api_key, openai_api_key

def fetch_pubmed_articles(user_data, user_input, max_results=3):
    """Fetches PubMed articles based on user input and medical data."""

    print("Inside PubMed Article Code")

    def extract_keywords(data, query, openai_api_key):
        """Extracts keywords using OpenAI GPT."""
        client = OpenAI(api_key=openai_api_key)
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """
                    Analyze user data and input to extract relevant medical keywords for PubMed search.
                    Keywords should relate to diseases, symptoms, deficiencies, or supplement-related topics.
                    Return only comma-separated keywords.
                    """},
                    {"role": "user", "content": f"User input: {data}\nUser profile: {query}"}
                ]
            )
            keywords = response.choices[0].message.content.strip()
            return [keyword.strip() for keyword in keywords.split(",") if keyword.strip()]
        except Exception as e:
            print(f"Warning: Failed to extract keywords. Error: {e}")
            return []  # Return empty list to prevent crash

    def query_pubmed_api(keyword, max_results, pubmed_api_key):
        """Queries PubMed API to retrieve article IDs for a given keyword."""
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": keyword,
            "retmax": max_results,
            "retmode": "json",
            "sort": "relevance",
            "api_key": pubmed_api_key,
        }
        for attempt in range(3):  # Retry mechanism with exponential backoff
            try:
                response = requests.get(base_url, params=params, timeout=10)
                if response.status_code == 200:
                    return response.json().get('esearchresult', {}).get('idlist', [])
                elif response.status_code == 429:  # API rate limit exceeded
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Warning: Error querying PubMed API ({response.status_code}). Skipping keyword.")
                    return []
            except requests.exceptions.RequestException as e:
                print(f"Warning: PubMed API request failed ({e}). Retrying...")
                time.sleep(2 ** attempt)
        print("Error: Max retries exceeded for PubMed API query.")
        return []  # Return empty list to prevent crash

    def fetch_article_details(article_ids, pubmed_api_key):
        """Fetches detailed information about articles from PubMed API."""
        if not article_ids:
            return []
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),
            "retmode": "xml",
            "api_key": pubmed_api_key,
        }
        for attempt in range(5):  # Retry mechanism with exponential backoff
            try:
                response = requests.get(base_url, params=params, timeout=10)
                if response.status_code == 200:
                    try:
                        tree = ElementTree.ElementTree(ElementTree.fromstring(response.content))
                        root = tree.getroot()
                        articles = []
                        for article in root.findall('.//PubmedArticle'):
                            title = article.find('.//ArticleTitle').text
                            abstract = article.find('.//Abstract/AbstractText').text if article.find('.//Abstract/AbstractText') is not None else "Abstract not available"
                            articles.append({
                                "title": title,
                                "abstract": abstract,
                            })
                        return articles
                    except Exception as e:
                        print(f"Warning: Error parsing PubMed article details ({e}). Skipping articles.")
                        return []
                elif response.status_code == 429:  # API rate limit exceeded
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Warning: Error fetching article details ({response.status_code}). Skipping articles.")
                    return []
            except requests.exceptions.RequestException as e:
                print(f"Warning: Request failed while fetching articles ({e}). Retrying...")
                time.sleep(2 ** attempt)
        print("Error: Max retries exceeded for fetching PubMed article details.")
        return []  # Return empty list to prevent crash

    # Main execution
    try:
        keywords = extract_keywords(user_data, user_input, openai_api_key)
        if not keywords:
            print("Warning: No keywords extracted. Exiting process.")
            return "No relevant articles found."

        all_articles = {}
        for keyword in keywords:
            keyword_with_context = keyword + " Supplement"
            article_ids = query_pubmed_api(keyword_with_context, max_results, pubmed_api_key)
            if not article_ids:
                print(f"Warning: No articles found for keyword '{keyword_with_context}'.")
                continue
            articles = fetch_article_details(article_ids, pubmed_api_key)
            if not articles:
                print(f"Warning: Unable to fetch details for articles on '{keyword_with_context}'.")
                continue
            all_articles[keyword_with_context] = articles

        if not all_articles:
            return "No relevant articles found."

        # Generate the customized prompt
        prompt = "Relevant PubMed Articles:\n"
        for keyword, articles in all_articles.items():
            prompt += f"Keyword: {keyword}\n"
            for article in articles:
                prompt += f"Title: {article['title']}\nAbstract: {article['abstract']}\n\n"
        return prompt
    except Exception as e:
        print(f"Critical Error: {e}")
        return "An error occurred while processing your request. Please try again later."
