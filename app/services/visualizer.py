# import matplotlib.pyplot as plt
# import pandas as pd
# import os
# import uuid

# OUTPUT_DIR = "charts"

# def generate_charts(df: pd.DataFrame) -> list[str]:
#     os.makedirs(OUTPUT_DIR, exist_ok=True)
#     image_paths = []

#     numeric_cols = df.select_dtypes(include='number').columns
#     for col in numeric_cols:
#         fig, ax = plt.subplots()
#         df[col].plot(kind='hist', ax=ax, title=f"Distribution of {col}")
#         chart_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.png")
#         plt.savefig(chart_path)
#         plt.close()
#         image_paths.append(chart_path)

#     return image_paths

import os, uuid
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List
from services.chart_spec import ChartSpec

OUTPUT_DIR = "charts"
sns.set_style("whitegrid")
FIGSIZE = (8, 4)

def _save(fig, name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}_{uuid.uuid4().hex}.png")
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

def render_chart(df: pd.DataFrame, spec: ChartSpec) -> str:
    typ = spec["type"]
    if typ == "time_series":
        date = spec["x"]
        y = spec["y"]
        df = df.sort_values(date)
        fig, ax = plt.subplots(figsize=FIGSIZE)
        ax.plot(df[date], df[y], marker="o")
        ax.set_title(f"{y} over time")
        ax.set_xlabel(date); ax.set_ylabel(y)
        return _save(fig, f"ts_{y}")

    if typ == "bar":
        x, y = spec["x"], spec["y"]
        top = spec.get("max_categories", 8)
        vc = df[x].value_counts().nlargest(top)
        fig, ax = plt.subplots(figsize=FIGSIZE)
        sns.barplot(x=vc.values, y=vc.index, ax=ax)
        ax.set_title(f"Bar: {x}")
        return _save(fig, f"bar_{x}")

    if typ == "histogram":
        col = spec["x"]
        fig, ax = plt.subplots(figsize=FIGSIZE)
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
        return _save(fig, f"hist_{col}")

    if typ == "heatmap":
        cols = spec.get("columns", df.select_dtypes("number").columns.tolist())
        corr = df[cols].corr()
        fig, ax = plt.subplots(figsize=(6, 6))
        sns.heatmap(corr, annot=True, cmap="vlag", center=0, ax=ax)
        ax.set_title("Correlation")
        return _save(fig, "heatmap")

    raise ValueError(f"Unknown chart type: {typ}")

def generate_charts(df: pd.DataFrame, specs: List[ChartSpec]) -> list[str]:
    paths = []
    for spec in specs:
        try:
            paths.append(render_chart(df, spec))
        except Exception as e:
            # log and skip bad specs
            print(f"Failed to render {spec}: {e}")
    return paths

