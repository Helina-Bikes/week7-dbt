from dagster import op, job
import subprocess

# --- Ops ---

@op
def scrape_telegram_data():
    # Place your scraping logic here, or call the script
    print("Scraping Telegram data...")
    # Example: subprocess.run(["python", "scrape.py"])
    return "scraped_data.json"

@op
def load_raw_to_mysql(scraped_file: str):
    print(f"Loading {scraped_file} into MySQL...")
    # Here you can call a Python function that inserts JSON into your raw_telegram_messages table
    return "loaded"

@op
def run_dbt_transformations():
    print("Running dbt transformations...")
    # Call dbt run command
    subprocess.run(["dbt", "run"], cwd="../telegram_project")  # adjust path if needed
    return "dbt_done"

@op
def run_yolo_enrichment():
    print("Running YOLO enrichment (optional)...")
    # Placeholder for any AI/image processing enrichment
    return "yolo_done"

# --- Job ---

@job
def telegram_pipeline_job():
    scraped = scrape_telegram_data()
    loaded = load_raw_to_mysql(scraped)
    transformed = run_dbt_transformations()
    enrichment = run_yolo_enrichment()
