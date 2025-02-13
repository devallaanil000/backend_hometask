# 🧪 PubMed Research Fetcher

## 📌 Description
This is a **Python CLI tool** that fetches research papers from **PubMed** and extracts papers with at least one **non-academic author** (affiliated with a pharma/biotech company). It also extracts the **corresponding author's email**.

## 🚀 Installation
### *
*1️ Clone the Repository**
```sh
git clone https://github.com/devallaanil000/backend_hometask.git
cd backend_hometask
2 Install Dependenciest
     poetry install
3 Usage
Run the CLI tool to fetch research papers:
    poetry run get-papers-list "cancer research" --file results.csv
4Additional Options
   -h or --help: Show usage instructionst
   poetry run get-papers-list --help
   -d or --debug: Enable debug mode

   poetry run get-papers-list "cancer research" -d
5 Features
✔ Fetches PubMed papers
✔ Identifies non-academic authors and their affiliations
✔ Extracts corresponding author emails
✔ Supports querying via CLI
✔ Outputs CSV format results
6🛠️ Dependencies
Python 3.9+
Poetry for package management
Requests for API calls
Typer for CLI handling
Pandas for CSV processing

7 Code Organization
src/pubmed_fetcher.py → Core logic to fetch & process PubMed data
src/cli.py → Command-line interface
tests/ → Unit tests
pyproject.toml → Poetry dependency manager
⚡ Bonus Features
✔ Breaks into a module & CLI program
✔ Can be published on TestPyPI

📜 License
This project is licensed under the MIT License.

🔹 **Save & Exit (`Ctrl + X`, `Y`, `Enter`)**  
🔹 **Push the README Update:**
```sh
git add README.md
git commit -m "Updated README with instructions"
git push origin main
