# Description

This project is designed to parse job postings from robota.ua using Selenium and save the results to a CSV file. It automates the collection of job information based on a given query (profession/keyword) and country.

# Setup

1. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .\.venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the **`.env`** file**:

   Create a `.env` file in the project root (based on `.env.example`) and specify:

   ```env
   VACANCY=Python           # Query for job search
   COUNTRY=Ukraine          # Country (in Latin script or localized as needed)
   REMOTE=False             # Find remote vacancies
   SUFFIX_FILE=_request     # Suffix for the output file name
   ```

   - `VACANCY`: the job title or keyword to search for.
   - `COUNTRY`: the country used in the URL query.
   - `SUFFIX_FILE`: additional text appended to the saved CSV file name.

4. **Ensure Firefox and Geckodriver are installed**:

   - Download Firefox from the official Mozilla website.
   - Download the appropriate Geckodriver version from GitHub ([https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)) and add it to your PATH.

# Usage

Run from the project root directory:

```bash
python -m src.__main__
```

Or:

```bash
python src/__main__.py
```
