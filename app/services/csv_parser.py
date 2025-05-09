import pandas as pd
import csv
import re
import os
from io import StringIO
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def create_structured_df(df: str) -> str:
    prompt = f"""You're a data engineer. You have been given aun unstructured csv. Your job is to process
    the unstructured raw csv into structured csv. Provide me the structured csv only after processing as output:
    \n\n{df}"""
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt
    )
    return response.text

def process_clean_csv(file_path: str):
    try:
        raw_csv = ''
        with open(file_path, "r", encoding="utf-8") as f:
            raw_csv = f.read()
        structurd_df = create_structured_df(raw_csv)
        lines = structurd_df.strip().splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        csv_data = "\n".join(lines)
        cleaned_csv = fix_unquoted_commas_in_numbers(csv_data)

        # Use csv.reader to normalize row lengths
        reader = csv.reader(StringIO(cleaned_csv))
        rows = list(reader)

        max_cols = max(len(row) for row in rows)
        col_names = [f"Col_{i}" for i in range(max_cols)]

        padded_rows = [row + [''] * (max_cols - len(row)) for row in rows]
        new_df = pd.DataFrame(padded_rows, columns=col_names)
        new_df = promote_first_row_as_header(new_df)
        new_df = convert_numeric_columns(new_df)
        return (csv_data,new_df)
    
    except Exception as e:
        raise ValueError(f"Error cleaning CSV: {e}")
    

def fix_unquoted_commas_in_numbers(text: str) -> str:
    # Match things like 12,000 or $10,500 and wrap them in double quotes
    return re.sub(r'(?<!")(\$?\d{1,3}(?:,\d{3})+)(?!")', r'"\1"', text)

def promote_first_row_as_header(df: pd.DataFrame) -> pd.DataFrame:
    if df.shape[0] < 2:
        return df
    if all(isinstance(x, str) and not x.strip().isdigit() for x in df.iloc[0]):
        df.columns = df.iloc[0]
        return df[1:].reset_index(drop=True)
    return df

def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.columns:
        try:
            # Only attempt conversion if the column is a 1-D object
            if isinstance(df[col], pd.Series):
                df[col] = pd.to_numeric(df[col], errors="ignore")
        except Exception as e:
            print(f"Skipping column {col}: {e}")
    return df