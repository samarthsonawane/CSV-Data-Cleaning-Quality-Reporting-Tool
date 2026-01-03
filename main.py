from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os

# ------------------ App Setup ------------------

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


UPLOAD_DIR = "uploads"
CLEANED_DIR = "cleaned"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CLEANED_DIR, exist_ok=True)

# ------------------ Home Route ------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# ------------------ Upload & Clean CSV ------------------

@app.post("/upload", response_class=HTMLResponse)
async def upload_csv(
    request: Request,
    file: UploadFile = File(...)
):
    # Read form values
    form_data = await request.form()
    numeric_strategy = form_data.get("numeric_strategy")
    categorical_strategy = form_data.get("categorical_strategy")

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Read CSV
    df = pd.read_csv(file_path)

    # -------- SUMMARY (BEFORE) --------
    rows_before = df.shape[0]
    missing_before = df.isna().sum().sum()

    # Column-wise missing values BEFORE cleaning
    missing_by_column_before = df.isna().sum().to_dict()

    # -------- Remove Duplicates --------
    df = df.drop_duplicates()
    rows_after_duplicates = df.shape[0]
    duplicates_removed = rows_before - rows_after_duplicates

    # -------- Identify Column Types --------
    numeric_cols = df.select_dtypes(include="number").columns
    categorical_cols = df.select_dtypes(include="object").columns

    # -------- Handle Numeric Missing Values --------
    if numeric_strategy == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    elif numeric_strategy == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    elif numeric_strategy == "mode":
        df[numeric_cols] = df[numeric_cols].fillna(
            df[numeric_cols].mode().iloc[0]
        )

    # -------- Handle Categorical Missing Values --------
    if categorical_strategy == "mode":
        df[categorical_cols] = df[categorical_cols].fillna(
            df[categorical_cols].mode().iloc[0]
        )
    else:
        df[categorical_cols] = df[categorical_cols].fillna("Not Available")

    # -------- Standardize Text --------
    for col in categorical_cols:
        df[col] = df[col].str.strip().str.lower()

    # -------- SUMMARY (AFTER) --------
    rows_after = df.shape[0]
    missing_after = df.isna().sum().sum()

    # Column-wise missing values AFTER cleaning
    missing_by_column_after = df.isna().sum().to_dict()

    # -------- Save Cleaned File --------
    cleaned_file_name = "cleaned_" + file.filename
    cleaned_file_path = os.path.join(CLEANED_DIR, cleaned_file_name)
    df.to_csv(cleaned_file_path, index=False)

    # -------- Summary Data --------
    summary = {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "duplicates_removed": duplicates_removed,
        "missing_before": missing_before,
        "missing_after": missing_after,
        "numeric_strategy": numeric_strategy,
        "categorical_strategy": categorical_strategy,
        "file_name": cleaned_file_name,
        "missing_by_column_before": missing_by_column_before,
        "missing_by_column_after": missing_by_column_after
    }

    return templates.TemplateResponse(
        "summary.html",
        {"request": request, "summary": summary}
    )

# ------------------ Download Cleaned File ------------------

@app.get("/cleaned/{filename}")
def download_cleaned_file(filename: str):
    file_path = os.path.join(CLEANED_DIR, filename)
    return FileResponse(
        file_path,
        media_type="text/csv",
        filename=filename
    )
