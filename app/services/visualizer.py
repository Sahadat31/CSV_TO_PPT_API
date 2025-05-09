import matplotlib.pyplot as plt
import pandas as pd
import os
import uuid

OUTPUT_DIR = "charts"

def generate_charts(df: pd.DataFrame) -> list[str]:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    image_paths = []

    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        fig, ax = plt.subplots()
        df[col].plot(kind='hist', ax=ax, title=f"Distribution of {col}")
        chart_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.png")
        plt.savefig(chart_path)
        plt.close()
        image_paths.append(chart_path)

    return image_paths
