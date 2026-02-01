import pandas as pd
from sqlalchemy import create_engine

yolo_df = pd.read_csv("yolo_results.csv")
engine = create_engine("postgresql://postgres:arwa1234@localhost:5432/medical_warehouse")
yolo_df.to_sql("raw_yolo_results", engine, if_exists="replace", index=False)
print(" YOLO results uploaded to PostgreSQL as 'raw_yolo_results'")