# 🩺 Medial Insight Platform

Welcome to the **Medial Insight Platform**! This project is designed to extract, process, and analyze data from Telegram using advanced data engineering and machine learning tools. This project delivers an end-to-end data platform that extracts and transforms public Telegram content related to Ethiopian medical businesses into structured, enriched insights. The pipeline automates data scraping, dimensional modeling, image analysis, and exposes analytical endpoints via a production-ready API. It's built with reproducibility, observability, and scalability at its core — suitable for driving health-tech analytics, competitive intelligence, and visual product tracking.

---

## 🚀 Project Structure

```
medial-insight-platform/
├── .env
├── initdb/
│   └── init.sql
├── data/
├── logs/
├── models/
├── screenshots/
├── src/
│   └── load.py
│   └── object_detection.py
│   └── schema.py
│   └── scrapper.py
├── medical_insight_dbt/
├── medical_insight_api/
├── medical_insight_pipeline/
├── docker-compose.yml
├── Dockerfile.dagster
├── Dockerfile.user_code
├── requirements.md
├── README.md
```

---

## 🛠️ Features & Technologies

- **Telegram Scraping**: Uses [Telethon](https://github.com/LonamiWebs/Telethon) to scrape data from Telegram.  
    - Credentials are stored securely in the `.env` file.
- **Database**: [PostgreSQL](https://www.postgresql.org/) is used for data storage.
    - Database tables are initialized via SQL scripts in `initdb/init.sql`.
    - The project is Dockerized for easy deployment.
- **Data Transformation**: [dbt](https://www.getdbt.com/) is used for transforming and modeling data.
    - All dbt models and configurations are under `medical_insight_dbt/`.
- **Object Detection**: [YOLO](https://github.com/ultralytics/yolov5) is integrated for image-based object detection.
- **API Interface**: [FastAPI](https://fastapi.tiangolo.com/) provides a RESTful API.
    - All API code is located in `medical_insight_api/`.
- **Orchestration**: [Dagster](https://dagster.io/) is used for workflow orchestration.
    - All pipelines and jobs are in `medical_insight_pipeline/`.

---

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medial-insight-platform.git
cd medial-insight-platform
```

### 2. Environment Variables

- Copy `.env.example` to `.env` and fill in your Telegram API credentials and other secrets.

### 3. Docker Setup

- Ensure you have [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed.
- Start the services:

```bash
docker-compose up --build
```

- This will:
    - Set up PostgreSQL and initialize tables using `initdb/init.sql`.
    - Build and run all services.

### 4. Database Initialization

- The database will be automatically initialized with the schema defined in `initdb/init.sql`.

### 5. Running dbt

- Navigate to `medical_insight_dbt/` and run:

```bash
dbt run
```

### 6. Running FastAPI

- The FastAPI app is in `medical_insight_api/`. It will be served via Docker Compose, or you can run it locally:

```bash
cd medical_insight_api
uvicorn main:app --reload
```

### 7. Running Dagster

- The orchestration pipelines are in `medical_insight_pipeline/`. To start Dagster UI:

```bash
cd medical_insight_pipeline
dagster dev
```

---

## 🧩 Directory Details

- **`.env`**: Environment variables for sensitive credentials.
- **`initdb/init.sql`**: SQL scripts to initialize PostgreSQL tables.
- **`medical_insight_dbt/`**: dbt models and configurations.
- **`medical_insight_api/`**: FastAPI application code.
- **`medical_insight_pipeline/`**: Dagster pipelines and orchestration code.

---

## 📝 Usage

- **Scrape Telegram**: Use the Telethon scripts to fetch data.
- **Store Data**: Data is stored in PostgreSQL.
- **Transform Data**: Use dbt to clean and model the data.
- **Detect Objects**: YOLO is used for object detection on images.
- **Access API**: Interact with the data and models via FastAPI endpoints.
- **Orchestrate Workflows**: Use Dagster to manage and schedule data pipelines.

---

## 🧑‍💻 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the Apache License.

---

## 📬 Contact

For questions or support, please open an issue or contact the maintainer.

---

Enjoy exploring the Medial Insight Platform! 🚀