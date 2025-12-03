# Referral Program Data Pipeline

## Overview
This project processes user referral data to identify successful referrals and detect potential fraud based on business logic. It transforms raw CSV data into a comprehensive marketing report.

## Project Structure
* `src/`: Contains the main ETL script (`main.py`).
* `data/`: Contains the raw input CSV files.
* `output/`: Stores the generated `final_marketing_report.csv`.
* `Dockerfile`: Configuration for containerizing the application.
* `requirements.txt`: Python dependencies.

## Prerequisites
* Docker (or Podman-Docker on Fedora)

## How to Run
This application is containerized for portability. Follow these steps to generate the report:

### 1. Build the Docker Image
```bash
docker build -t de-project .
