import subprocess
import os
from dagster import op, job, schedule, RunConfig


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PYTHON_EXE = os.path.join(PROJECT_ROOT, "venvm", "Scripts", "python.exe")

@op(description="Runs the Python scraper script using the venvm executable.")
def scrape_telegram_data():
    script_path = os.path.join(PROJECT_ROOT, "src", "scraper.py")

    subprocess.run([PYTHON_EXE, script_path], check=True)
    return True

@op(description="Loads raw data into PostgreSQL.")
def load_raw_to_postgres(success: bool):
    if success:
        script_path = os.path.join(PROJECT_ROOT, "src", "database_load.py")
        subprocess.run([PYTHON_EXE, script_path], check=True)
    return True

@op(description="Triggers dbt transformations.")
def run_dbt_transformations(success: bool):
    if success:
        dbt_exe = os.path.join(PROJECT_ROOT, "venvm", "Scripts", "dbt.exe")
        dbt_project_path = os.path.join(PROJECT_ROOT, "medical_warehouse")
        
        subprocess.run([dbt_exe, "run"], cwd=dbt_project_path, check=True)
    return True

@op(description="Runs YOLOv8 object detection and uploads results.")
def run_yolo_enrichment(success: bool):
    if success:
      
        detect_script = os.path.join(PROJECT_ROOT, "src", "yolo_detect.py")
        subprocess.run([PYTHON_EXE, detect_script], check=True)
        
       
        upload_script = os.path.join(PROJECT_ROOT, "src", "upload_yolo.py")
        subprocess.run([PYTHON_EXE, upload_script], check=True)



@job(description="The end-to-end medical data pipeline.")
def medical_data_pipeline():
    scraped = scrape_telegram_data()
    loaded = load_raw_to_postgres(scraped)
    transformed = run_dbt_transformations(loaded)
    run_yolo_enrichment(transformed)

@schedule(
    cron_schedule="0 0 * * *",  
    job=medical_data_pipeline,
    execution_timezone="UTC",
)
def daily_medical_pipeline_schedule():
    return RunConfig()