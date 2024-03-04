import requests
from bs4 import BeautifulSoup
import re

# List of company domains
companies = [
    "pitcs.in",
    "joyitsolutions.co",
    "peepalconsulting.com",
    "pradeepit.com",
    "mekhalyn.com",
    "insightconsultants.co",
    "ascent-hr.com",
    "siemens.com",
    "dexteronweb.com"
]

# Replace this with your actual User-Agent
headers = {'User-Agent': 'Your User-Agent Here'}

def fetch_links_for_company(company):
    """Fetches links for a specific company related to 'financial report'."""
    query = f'site:{company} "financial" OR "report" OR "statement"'
    url = f'https://www.google.com/search?q={query}'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/url?q=' in href and not 'webcache' in href:
            actual_url = href.split('&')[0].split('/url?q=')[1]
            links.append(actual_url)
    return links

def classify_link_relevance(url):
    """Classifies a link's relevance to financial reports or statements."""
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.body.get_text(separator=' ', strip=True).lower()
        if "financial report" in text or "financial statement" in text:
            return "High"
        elif "financial" in text:
            return "Medium"
        else:
            return "Low"
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return "Error"

def categorize_company_links(companies):
    """Categorizes links for each company based on their relevance."""
    company_categories = {}
    for company in companies:
        links = fetch_links_for_company(company)
        categories = {"High": [], "Medium": [], "Low": []}
        for link in links:
            category = classify_link_relevance(link)
            if category in categories:
                categories[category].append(link)
        company_categories[company] = categories
    return company_categories

# Due to the nature of live scraping and requests to external sites, execute cautiously and respect usage limits.
company_links_categorized = categorize_company_links(companies[:1])  # Limiting to the first company for demonstration

# Display the categorized links for the company
for company, categories in company_links_categorized.items():
    print(f"Company: {company}")
    for category, links in categories.items():
        print(f"Category: {category}")
        for link in links:
            print(f"- {link}")
        print("\n")
