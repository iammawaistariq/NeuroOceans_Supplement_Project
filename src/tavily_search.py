from tavily import TavilyClient
from utils.config import Tavily_API_key

# Tavily function to return images and results without filtering by unique domains
def tavily_search_and_extract(product_name_with_brand, max_results=5, include_images=False):
    try:
        tavily_client = TavilyClient(api_key=Tavily_API_key)
        tavily_response = tavily_client.search(
            query=product_name_with_brand,
            max_results=max_results,  # Fetch only the required number of results
            search_depth="basic",
            topic="general",
            include_domains = [
                "amazon.com",  # Most popular and trusted online retailer
                "thorne.com",  # NSF-certified, used by professionals and athletes
                "lifeextension.com",  # High-quality, research-backed formulations
                "nowfoods.com",  # Well-established, affordable, and high-quality
                "gardenoflife.com",  # Organic, whole-food-based supplements
                "nordic.com",  # Premium omega-3 and essential nutrient provider
                "kleanathlete.com",  # Sports-certified, used by professional athletes
                "nutrabio.com",  # Transparent labeling, high-quality standards
                "gaiaherbs.com",  # Trusted for herbal and botanical supplements
                "solgar.com",  # Premium, long-established supplement brand
                "naturesway.com",  # Trusted herbal and dietary supplement brand
                "doctorsbest.com",  # Science-backed and research-driven
                "optimumnutrition.com",  # High-quality sports and fitness supplements
                "transparentlabs.com",  # Clean ingredients, no artificial additives
                "barleans.com",  # Best known for high-quality oils and omega-3s
                "doublewoodsupplements.com",  # Trusted nootropic and cognitive health brand
                "nootropicsdepot.com",  # Specialized in high-purity cognitive enhancers
                "seekinghealth.com",  # Functional medicine, genetic-based supplementation
                "tryarmra.com",  # High-quality colostrum-based wellness supplements
                "vitalnutrients.co",  # Practitioner-recommended, high-quality formulas
                "natrol.com",  # Popular for sleep and mood support supplements
                "carlylenutritionals.com",  # Well-reviewed, cost-effective alternative
                "sourcenaturals.com",  # Trusted science-based supplement formulations
                "costco.com",  # Bulk retailer with strict quality control
                "swansonvitamins.com",  # Budget-friendly, large selection
                "bulksupplements.com",  # Raw ingredients, good for customization
                "bluebonnetnutrition.com",  # Organic, clean-label supplements
                "amix-nutrition.com",  # European brand, high in sports nutrition
                "whynotnatural.com",  # Smaller but focused on clean, natural ingredients
                "meonutrition.com",  # Niche, high-quality performance supplements
                "santacruzpaleo.com",  # Paleo and keto-friendly supplements
                "toniiq.com",  # High-potency and purity-focused specialty supplements
                "pureforyou.com",  # Niche brand, limited recognition
                "livemomentous.com",  # Athlete-focused, performance supplements
                "naturesbounty.com",  # Mass-market, mixed reputation on ingredient quality
                "allinnutritionals.com",  # Lesser-known brand with limited reviews
                "caltrate.com",  # Focused only on calcium, limited product range
                "citracal.com"  # Bone health-focused, but not a broad supplement brand
                ],
            include_images=include_images
        )

        # Extract only 'images' and 'results'
        image_url = tavily_response.get("images", [])
        results = tavily_response.get("results", [])
        # Return the final dictionary
        return {
            "Image URL": image_url,
            "results": results
        }
    except Exception as e:
        print(f"Error occurred during Tavily search: {str(e)}")
        return {
            "Image URL": [],
            "results": []
        }
