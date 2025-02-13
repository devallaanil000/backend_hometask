import requests
import xml.etree.ElementTree as ET
import pandas as pd
from typing import List, Dict, Tuple

# PubMed API URLs
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_pubmed_ids(query: str, max_results: int = 20) -> List[str]:
    """Fetch PubMed IDs based on a search query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "xml",
        "retmax": max_results
    }
    response = requests.get(PUBMED_API_URL, params=params)
    root = ET.fromstring(response.content)

    return [id_elem.text for id_elem in root.findall(".//Id")]

def extract_publication_date(article) -> str:
    """Extract the publication date from a PubMed article."""
    pub_date_elem = article.find(".//PubDate")
    if pub_date_elem is not None:
        return " ".join([elem.text for elem in pub_date_elem if elem.text])
    return "N/A"

def extract_corresponding_author_email(article) -> str:
    """Extract the corresponding author's email from the PubMed article."""
    for affiliation in article.findall(".//AffiliationInfo"):
        email_elem = affiliation.find(".//Affiliation")
        if email_elem is not None and "@" in email_elem.text:
            return email_elem.text.strip()
    return "N/A"

def extract_non_academic_authors(article) -> Tuple[List[str], List[str]]:
    """Extract non-academic authors by checking their affiliations."""
    non_academic_authors = []
    company_affiliations = []

    for author in article.findall(".//AuthorList/Author"):
        last_name = author.find("LastName")
        fore_name = author.find("ForeName")
        affiliation_elem = author.find(".//AffiliationInfo/Affiliation")

        if last_name is not None and affiliation_elem is not None:
            affiliation_text = affiliation_elem.text.strip().lower()
            author_name = f"{fore_name.text} {last_name.text}" if fore_name is not None else last_name.text
            
            company_keywords = [
                "inc", "ltd", "pharma", "biotech", "corporation", "laboratories", 
                "solutions", "systems", "technologies", "gmbh", "s.a.", "limited", 
                "therapeutics", "diagnostics", "lifesciences", "biosciences", 
                "biopharma", "biotherapeutics", "genomics", "biomedical"
            ]
            academic_keywords = [
                "university", "hospital", "research center", "faculty", "department", 
                "school", "institute", "foundation", "clinic", "medicity"
            ]

            if any(keyword in affiliation_text for keyword in company_keywords) and not any(keyword in affiliation_text for keyword in academic_keywords):
                non_academic_authors.append(author_name)
                company_affiliations.append(affiliation_elem.text.strip())

    return non_academic_authors, company_affiliations

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch detailed paper information from PubMed using IDs."""
    if not pubmed_ids:
        return []

    params = {"db": "pubmed", "id": ",".join(pubmed_ids), "retmode": "xml"}
    response = requests.get(PUBMED_FETCH_URL, params=params)
    root = ET.fromstring(response.content)

    papers = []
    for article in root.findall(".//PubmedArticle"):
        pubmed_id_elem = article.find(".//PMID")
        pubmed_id = pubmed_id_elem.text if pubmed_id_elem is not None else "N/A"

        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text.strip() if title_elem is not None and title_elem.text else "N/A"

        pub_date = extract_publication_date(article)
        non_academic_authors, company_affiliations = extract_non_academic_authors(article)
        email = extract_corresponding_author_email(article)  # ✅ Added this line

        papers.append({
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-Academic Authors": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "None",
            "Corresponding Author Email": email
        })

    return papers

def save_to_csv(papers: List[Dict], filename: str):
    """Save the extracted papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)

