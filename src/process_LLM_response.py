import json
from src.tavily_search import tavily_search_and_extract
from urllib.parse import urlparse

def process_llm_response(llm_response):

    print("4. Preprocessing LLM response")
    
    """
    Process LLM response to include exactly 3 URLs: prioritize Amazon if available, followed by other unique domains.
    """
    def is_amazon_product_url(url):
        """Check if a URL is a valid Amazon product page."""
        
        parsed_url = urlparse(url)

        return "amazon" in parsed_url.netloc and "/dp/" in parsed_url.path

    def extract_source_name(url):
        """Extract the source name from a URL."""
        return urlparse(url).netloc.replace("www.", "").split('.')[0].title()

    def filter_unique_domains(url_list):
        """Filter URLs to ensure unique domains."""
        seen_domains = set()
        unique_urls = []
        for item in url_list:
            domain = urlparse(item["url"]).netloc
            if domain not in seen_domains:
                seen_domains.add(domain)
                unique_urls.append(item)
        return unique_urls

    try:
        # Parse the LLM response
        response_json = json.loads(llm_response)
        print("Raw LLM Response:", response_json)

        # Check if "supplements" key exists in the response
        supplements = response_json.get("supplements", [])
        
        # Iterate over each supplement in the list
        for supplement in supplements:
            # Extract product name from the 'medical_grade_supplements' section
            product_name = supplement.get("medical_grade_supplements", {}).get("product_name_and_brand")
            print(f"Processing Product: {product_name}")
            
            # Skip if product name is missing
            if not product_name:
                continue

            try:
                # Call Tavily API to search for product details (URLs, images, etc.)
                tavily_results = tavily_search_and_extract(product_name, max_results=10, include_images=True)
                print(f"results for {product_name}",tavily_results)
                
                # Extract image URL if available
                image_url = tavily_results.get("Image URL")[0] if tavily_results.get("Image URL") else None
                
                # Extract product results (URLs and other info)
                product_results = tavily_results.get("results", [])

                # Separate Amazon URLs first (whether valid product URLs or not)
                all_amazon_urls = [result["url"] for result in product_results if "amazon" in result.get("url", "").lower()]

                # Now filter valid Amazon product URLs
                amazon_product_urls = [url for url in all_amazon_urls if is_amazon_product_url(url)]

                # Extract non-Amazon URLs (ensuring they don't include any Amazon URLs)
                non_amazon_urls = [
                    {"name": extract_source_name(result["url"]), "url": result["url"]}
                    for result in product_results
                    if result.get("url", "") not in all_amazon_urls  # Exclude ALL Amazon URLs
                ]

                # Deduplicate domains in non-Amazon URLs
                non_amazon_urls = filter_unique_domains(non_amazon_urls)

                # Prepare the product URL list (always 3 URLs - prioritize Amazon product URLs if present)
                if amazon_product_urls:
                    product_url_list = [{"name": "Amazon", "url": amazon_product_urls[0]}] + non_amazon_urls[:2]
                else:
                    product_url_list = non_amazon_urls[:3]
                
                print(f"Selected product URLs {product_url_list}")

                # Add the gathered details to the supplement dictionary
                if image_url:
                    print("Image URLs found")
                    supplement["medical_grade_supplements"]["Image URL"] = image_url
                
                supplement["medical_grade_supplements"]["Product URL"] = product_url_list

            except Exception as e:
                print(f"Error processing supplement '{product_name}': {str(e)}")
                continue

        # Return the updated response JSON
        return response_json

    except Exception as e:
        print(f"Error processing LLM response: {str(e)}")
        return {}
