import typer
from src.pubmed_fetcher import fetch_pubmed_ids, fetch_paper_details, save_to_csv

app = typer.Typer()

@app.command()
def fetch_papers(query: str, file: str = None):
    """Fetch PubMed papers and save to CSV."""
    pubmed_ids = fetch_pubmed_ids(query)
    papers = fetch_paper_details(pubmed_ids)

    if file:
        save_to_csv(papers, file)
        print(f"Results saved to {file}")
    else:
        print(papers)

if __name__ == "__main__":
    app()

