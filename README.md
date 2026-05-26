# Job Search Analyzer
![Python](https://img.shields.io/badge/python-3.12-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)

![CI](https://github.com/AndrewKchn/job-search-analyzer/actions/workflows/tests.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-80%25-green)
---



A data-driven job market analytics application built with Streamlit. 

🔗 Live Demo: https://job-search-analyzer-nhphyrewtee3uq4xnsy9l7.streamlit.app/

The project collects job listings from an external API, stores them in a database, and provides interactive analytics, filtering, and trend visualization.

---

## 📊 Overview

Job Search Analyzer is a lightweight analytics tool designed to explore job market trends, filter job listings, and analyze hiring patterns over time.

Unlike traditional web applications, this project is built entirely on Streamlit, meaning the UI and backend logic run within the same Python runtime. Business logic is separated into service and repository layers to maintain clean architecture and testability.

---

## ✨ Features

- 🔄 Automatic job synchronization from external API (Arbeitnow)
- 📊 Interactive analytics dashboard
- 🔍 Advanced filtering (location, remote, keyword search)
- 📈 Daily, weekly, and monthly job trends
- 🏢 Company and location insights
- ⚡ Cached data loading for improved performance
- 🧪 Test coverage with pytest
- 🧱 Clean layered architecture (UI / Service / Repository)

---
## 🏗️ Architecture

The system follows a clean layered architecture:

![Architecture Diagram](docs/architecture.png)

PlantUML source: [architecture.puml](docs/architecture.puml)

### Design Principles
- Separation of concerns between UI, business logic, and data access
- Dependency inversion via repository interfaces
- Stateless service layer for testability and scalability
- External API encapsulation via dedicated client

### Layers
- UI Layer (Streamlit)\
  Handles rendering and user interaction only.
- Service Layer\
  Contains all business logic:
  - Sync orchestration
  - Analytics computation
  - Trend generation
- Infrastructure Layer\
  Responsible for:
  - Database access (PostgreSQL / SQLite)
  - External API communication
  - ORM mapping

---

## 🧠 System Design

### Overview

This application is designed as a lightweight analytics system built on top of Streamlit. Unlike traditional web applications, it does not use a separate frontend/backend split with REST APIs. Instead, Streamlit executes Python code directly and renders the UI based on the execution result.

### Data Flow (Sync Process)

![Sync Sequence Diagram](docs/sync_sequence.png)

PlantUML source: [sync_sequence.puml](docs/sync_sequence.puml)

### Design Decisions

#### 1. Streamlit as UI + Runtime

Instead of separating frontend and backend, Streamlit is used as a unified runtime layer. 
This simplifies deployment but still allows clean architectural separation inside the codebase.

#### 2. Service-Oriented Design

Business logic is isolated in services to:

- Avoid coupling with UI framework
- Enable unit testing without Streamlit
- Prepare for future backend migration

#### 3. Repository Pattern

All database access is abstracted behind repositories to:

- Decouple persistence logic from business logic
- Allow database switching without service changes
- Enable mocking in tests

#### 4. Trade-offs

| Decision                             | Trade-off                             |
| ------------------------------------ | ------------------------------------- |
| Streamlit instead of React + FastAPI | Faster development, less scalability  |
| Sync-based ingestion                 | Simplicity over real-time streaming   |
| Pandas-based analytics               | Flexibility over performance at scale |

---

## 🛠️ Tech Stack

- Streamlit – UI framework
- Pandas – data processing and analytics
- SQLAlchemy – ORM
- PostgreSQL / SQLite – database
- Requests – external API integration
- Pytest – testing framework
- Loguru – logging

---

## 🚀 Installation

Clone the repository:
```
git clone https://github.com/AndrewKchn/job-search-analyzer.git
cd job-search-analyzer
```
Create virtual environment:
```
python -m venv .venv
source .venv/bin/activate  (Mac/Linux)
.venv\Scripts\activate     (Windows)
```
Install dependencies:
```
pip install -r requirements.txt
```

Run the application:
```
streamlit run streamlit_app.py
```
> Note: On first launch, Streamlit may display a welcome prompt in the terminal asking for an email address.  
> You can simply press `Enter` to continue without providing one.
---

## 📌 Usage

After launching the app:

- Open the sidebar to sync latest jobs
- Use filters to narrow down results
- Explore job analytics in the dashboard
- Switch between daily, weekly, and monthly trends tabs

Example workflow:

- Click "Sync Jobs" to fetch latest data
- Apply filters (location, remote, keyword)
- View updated analytics and trends instantly

---

## 🧱 Project Structure
```
job_analyzer/
├── ui/                  # Streamlit UI components
├── services/            # Business logic layer
├── infrastructure/      # DB and external API clients
├── models/              # DTOs and schemas
├── core/                # Interfaces and config
├── bootstrap.py         # Dependency setup
streamlit_app.py         # Application entry point
.github/workflows/       # GitHub Actions (tests, scheduled sync)
```
---

## 🧪 Testing Strategy

Current test coverage focuses on:
- Service layer logic
- Repository queries
- UI rendering behavior

Run tests with:
```
pytest --cov=job_analyzer --cov-report=term-missing
```
---
## ⚙️ CI/CD & Automation Pipelines

The project includes two GitHub Actions workflows to ensure code quality and automate data synchronization.

### 🧪 Python CI Pipeline

This pipeline runs on every pull request and ensures code quality by:

- Running automated tests (pytest)
- Checking test coverage thresholds
- Preventing merges if coverage drops below the defined limit

This ensures that all changes maintain a minimum level of reliability and test coverage.

---

### 🔄 Data Synchronization Pipeline

A scheduled GitHub Actions workflow responsible for:

- Periodic job data synchronization from the external API (Arbeitnow)
- Updating the database automatically without manual intervention

This allows the system to stay up-to-date even without user interaction.

---

## 🚧 Future Improvements
- Migration to FastAPI backend architecture
- Background job processing (async sync pipeline)
- Skill extraction from job descriptions (NLP)
- User authentication & personalization
- Cloud deployment (Docker + CI/CD)

---

## 🤝 Engineering Notes

This project is intentionally designed to demonstrate:

- Clean architecture principles in a lightweight environment
- Separation between UI and domain logic even without a backend API
- Scalability path toward distributed backend system design

---

## 📄 License

Educational project