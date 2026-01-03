# CSV Data Cleaning & Quality Reporting Tool

This project is a small web application built using FastAPI that helps clean CSV files by handling common data quality issues such as missing values and duplicate rows.

The goal of this project is to demonstrate practical data preprocessing logic that is commonly required before analysis or reporting.

---

## Features

- Upload CSV files through a web interface  
- Choose how missing values should be handled:
  - Numeric columns: mean, median, or mode  
  - Categorical columns: mode or a default value  
- Remove duplicate rows automatically  
- Standardize text data for consistency  
- Generate a summary showing:
  - Number of rows before and after cleaning  
  - Missing values before and after processing  
  - Duplicate rows removed  
- View a column-wise missing value report  
- Download the cleaned CSV file  

---

## Technology Used

- Python  
- FastAPI  
- Pandas  
- HTML and CSS  

---

## Running the Project Locally

Install the required dependencies:

```bash
pip install -r requirements.txt

```
Start the application by running:
```bash
uvicorn main:app --reload
```
Open the application in your browser:

```bash
http://127.0.0.1:8000
```

---

## Why This Project

In real-world scenarios, CSV files often contain missing or inconsistent data. Before any analysis or reporting, this data needs to be cleaned and validated.

This project focuses on automating common data cleaning steps in a simple and configurable way. The implementation avoids unnecessary complexity and focuses on clarity, correctness, and practical usage.

---
## Live Demo

Live application: https://csv-data-cleaning-tool.onrender.com
