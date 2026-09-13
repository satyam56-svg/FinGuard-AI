# FinGuard AI — AI Powered Fraud Detection System

[🚀 Live Demo](https://finguard-ai-4ico.onrender.com) | [Spring Boot Backend API](https://finguard-ai-spring.onrender.com) | [FastAPI ML Bridge](https://finguard-ai-backend-60wj.onrender.com)

**FinGuard AI** is an enterprise-grade financial fraud detection and risk assessment platform. It evaluates payment transactions in real time using a trained Random Forest machine learning classifier, computes deterministic risk scores and levels, generates SHAP feature-level explainability, and produces structured AI analyst reports powered by Google Gemini 2.5 Flash.

The production system architecture features a **React SPA frontend**, a robust **Spring Boot backend** handling security, authentication, RBAC, and audit persistence via **Neon PostgreSQL**, and a lightweight **FastAPI ML Bridge** dedicated to model inference and AI report generation.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Risk Engine](#risk-engine)
- [Explainability](#explainability)
- [AI Report Generation](#ai-report-generation)
- [API Documentation](#api-documentation)
- [Authentication & Authorization](#authentication--authorization)
- [Database Architecture](#database-architecture)
- [Admin Bootstrap Mechanism](#admin-bootstrap-mechanism)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Local Development](#local-development)
- [Production Deployment](#production-deployment)
- [Security](#security)
- [Testing](#testing)
- [Current Status](#current-status)

---

## Overview

Detecting financial transaction fraud requires real-time execution, precise risk scoring, feature-level transparency, and operational auditability. FinGuard AI fulfills these requirements through a decoupled microservice architecture:

1. **Submission**: The user submits payment transaction details (type, amount, balance states) via the React frontend.
2. **Gateway & Security**: The request reaches the Spring Boot backend, which authenticates the user via JWT, validates account status, and enforces Role-Based Access Control (RBAC).
3. **ML Inference & Explainability**: Spring Boot forwards the transaction payload to the FastAPI ML Bridge, which executes the ML pipeline:
   - Feature engineering and preprocessing via scikit-learn `ColumnTransformer`.
   - Fraud probability prediction using the trained `RandomForestClassifier`.
   - Deterministic risk assessment (0–100 score, categorical risk level, recommended action).
   - SHAP `TreeExplainer` feature-level risk and protective factor extraction with human-readable labels.
   - Constrained AI report synthesis powered by **Google Gemini 2.5 Flash** (`gemini-2.5-flash`).
4. **Audit & Response**: FastAPI returns the prediction result to Spring Boot. Spring Boot persists the prediction audit log into **Neon PostgreSQL** and delivers the payload back to the React UI.

---

## Key Features

### Fraud Detection & Risk Scoring
- Real-time transaction assessment via Spring Boot `/predict` endpoint.
- Trained Random Forest model configured with class imbalance mitigation.
- Configurable decision threshold (default: `0.60`).
- Continuous fraud probability (`0.0` to `1.0`).
- Normalized risk score (`0.0` to `100.0`, calculated as `fraud_probability × 100`).
- Categorical risk level: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
- Actionable decision recommendations: `ALLOW`, `ALLOW_WITH_MONITORING`, `REVIEW`, `BLOCK_OR_REVIEW`.

### Explainable AI (SHAP)
- Feature contribution analysis using SHAP `TreeExplainer`.
- Top risk factors (features increasing fraud probability).
- Top protective factors (features decreasing fraud probability).
- Human-readable feature naming mapping internal pipeline terms to intuitive domain descriptions (e.g. `"Origin balance pattern"`).
- Quantified impact metrics and direction indicator (`increases_fraud_risk` vs `reduces_fraud_risk`).

### AI Report Generation
- AI analyst summary powered by **Google Gemini 2.5 Flash** (`gemini-2.5-flash`).
- Strict JSON schema enforcement via Pydantic (`summary`, `risk_reason`, `recommended_action`).
- Constrained prompt guardrails: Gemini purely explains existing ML results and cannot alter probabilities, risk scores, levels, or recommendations.

### Security, Authentication & Role Management
- User registration and authentication with BCrypt password hashing.
- Stateless JWT issuance (HS256 signature).
- Role-Based Access Control (RBAC) with three tiers: `USER`, `ANALYST`, and `ADMIN`.
- Account active/inactive status enforcement on every authenticated endpoint.
- Admin self-protection server-side rules preventing admins from deactivating or revoking their own admin access.
- Startup admin account bootstrapper based on environment configuration.

### Dashboard & Audit
- User-level prediction history (`/predictions/history`).
- Analyst dashboard metrics (`total_predictions`, `fraud_predictions`, `non_fraud_predictions`, `fraud_rate`, `average_risk_score`).
- Analyst risk distribution breakdown across risk tiers (`low`, `medium`, `high`, `critical`).
- Analyst recent predictions feed.
- Admin User Management Console (list users, modify user roles, activate/deactivate accounts).

---

## System Architecture

```
                       ┌──────────────────────────────────┐
                       │          React Frontend          │
                       │ (https://finguard-ai-4ico... )   │
                       └────────────────┬─────────────────┘
                                        │
                                        │ REST API / JWT
                                        ▼
                       ┌──────────────────────────────────┐
                       │        Spring Boot Backend       │
                       │ (https://finguard-ai-spring... ) │
                       └───────┬──────────────────┬───────┘
                               │                  │
           Application Data /  │                  │ REST Proxy
             Audit Persistence │                  │ (/predict)
                               ▼                  ▼
┌────────────────────────────────┐      ┌──────────────────────────────────┐
│    Neon PostgreSQL Database    │      │        FastAPI ML Bridge         │
│     (Users & Audit Logs)       │      │ (https://finguard-ai-backend... )│
└────────────────────────────────┘      └────────────────┬─────────────────┘
                                                         │
                                                         ▼
                                                Python ML Pipeline
                                        ┌──────────────────────────────────┐
                                        │ ├── FraudPreprocessor            │
                                        │ ├── RandomForestClassifier       │
                                        │ ├── RiskEngine                   │
                                        │ ├── FraudExplainer (SHAP)        │
                                        │ └── AIReportGenerator (Gemini)   │
                                        └──────────────────────────────────┘
```

---

## Technology Stack

### Backend Service (Application & Auth Gateway)
| Component | Technology | Description |
|---|---|---|
| Language | Java 17 | Core backend runtime |
| Framework | Spring Boot 3.x | Web API framework |
| Security | Spring Security | Security filter chain and authorization rules |
| Authentication | JWT (jjwt) | Stateless JWT creation and validation |
| Password Hashing | BCrypt | Password encryption |
| Data Access | Spring Data JPA / Hibernate | ORM and persistence abstraction |
| HTTP Client | Spring RestClient | High-performance synchronous client for FastAPI bridge |

### ML Bridge & Pipeline Service
| Component | Technology | Description |
|---|---|---|
| Language | Python 3.11 | ML runtime environment |
| Framework | FastAPI | Async REST API framework for ML model |
| Server | Uvicorn | ASGI web server |
| Machine Learning | scikit-learn | RandomForestClassifier & ColumnTransformer preprocessor |
| Explainability | SHAP | TreeExplainer for feature importance analysis |
| Generative AI | Google Gemini 2.5 Flash | `google-genai` client for structured report generation |
| Data Processing | pandas, NumPy, joblib | Data matrix handling and artifact serialization |
| Schema Validation | Pydantic v2 | Fast strict schema validation |

### Frontend Application
| Component | Technology | Description |
|---|---|---|
| Framework | React 19 | Component-based UI library |
| Build Tool | Vite | Fast frontend build server |
| Language | JavaScript (ES2022+) | Application logic |
| Styling | Vanilla CSS | Responsive custom styling system |
| Icons | Lucide React | Modern icons |

### Database & Storage
| Database | Mode | Description |
|---|---|---|
| **Neon PostgreSQL** | **Production** | Managed cloud PostgreSQL database for production environment |
| **SQLite** | **Local Fallback** | File-based local database fallback (`finguard.db`) managed via Hibernate |

---

## Machine Learning Pipeline

### Dataset Contract & Feature Engineering
The model is trained on the **PaySim** financial transaction dataset. Input payloads accept 12 features, including 4 engineered balance-consistency features:

| Engineered Feature | Calculation Formula | Purpose |
|---|---|---|
| `origin_balance_error` | `oldbalanceOrg - amount - newbalanceOrig` | Detects post-transaction origin balance discrepancies |
| `destination_balance_error` | `oldbalanceDest + amount - newbalanceDest` | Detects post-transaction destination balance discrepancies |
| `origin_balance_change` | `oldbalanceOrg - newbalanceOrig` | Net amount debited from origin account |
| `destination_balance_change` | `newbalanceDest - oldbalanceDest` | Net amount credited to destination account |

### Preprocessing & Artifacts
- **Numeric Features (11 columns)**: Imputed with median strategy via scikit-learn `SimpleImputer`.
- **Categorical Feature (`type`)**: Encoded via `OneHotEncoder(handle_unknown="ignore")`.
- Fitted preprocessing transformer is serialized at `ml_pipeline/models/preprocessor.pkl`.

### Train / Validation / Test Split
- **Training**: 70%
- **Validation**: 15%
- **Test**: 15%

### Model Selection
Evaluated classifiers during training: Logistic Regression, Decision Tree, Random Forest, XGBoost, and LightGBM.  
The production deployment utilizes `ml_pipeline/models/random_forest.pkl` (`RandomForestClassifier` with class-weight balancing).

---

## Risk Engine

The `RiskEngine` (`ml_pipeline/risk/risk_engine.py`) derives deterministic risk scores and categories directly from the raw fraud probability.

- **Risk Score**: `round(fraud_probability * 100.0, 2)` (Scale: 0.0 to 100.0)
- **Decision Threshold**: `0.60` (Default configured in `MLConfig`)

| Fraud Probability Range | Risk Level | Recommendation |
|---|---|---|
| `< 0.20` | `LOW` | `ALLOW` |
| `0.20` to `< 0.40` | `MEDIUM` | `ALLOW_WITH_MONITORING` |
| `0.40` to `< 0.60` | `HIGH` | `REVIEW` |
| `≥ 0.60` | `CRITICAL` | `BLOCK_OR_REVIEW` |

---

## Explainability

SHAP (`shap.TreeExplainer`) analyzes individual transaction predictions:
1. Computes feature contribution values for the preprocessed transaction matrix.
2. Formats top 5 **risk factors** (positive SHAP values pushing risk higher).
3. Formats top 5 **protective factors** (negative SHAP values pushing risk lower).
4. Translates raw column keys to human-readable names (e.g., `numeric__origin_balance_error` → `Origin balance pattern`).

---

## AI Report Generation

`AIReportGenerator` invokes **Google Gemini 2.5 Flash** (`gemini-2.5-flash`) via the `google-genai` SDK:
- Enforces strict JSON return structure conforming to:
  ```json
  {
    "summary": "Analyst summary text...",
    "risk_reason": "Detailed risk reasoning...",
    "recommended_action": "ALLOW | ALLOW_WITH_MONITORING | REVIEW | BLOCK_OR_REVIEW"
  }
  ```
- Prompt guardrails ensure Gemini does not recalculate scores or override ML model outputs.

---

## API Documentation

### Spring Boot Backend Services (Primary Gateway)

#### 1. Health
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `GET` | `/health` | No | Any | Backend service status |

#### 2. Authentication
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `POST` | `/auth/register` | No | Any | Register new account (default role: `USER`) |
| `POST` | `/auth/login` | No | Any | Authenticate and obtain JWT access token |

**Register Request**:
```json
{
  "username": "analyst_user",
  "email": "analyst@example.com",
  "password": "strongpassword123"
}
```

**Login Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni..."
}
```

#### 3. Fraud Prediction
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `POST` | `/predict` | Bearer JWT | `USER`, `ANALYST`, `ADMIN` | Submit transaction for fraud evaluation & audit |

**Transaction Request Payload**:
```json
{
  "step": 1,
  "type": "TRANSFER",
  "amount": 181.0,
  "oldbalanceOrg": 181.0,
  "newbalanceOrig": 0.0,
  "oldbalanceDest": 0.0,
  "newbalanceDest": 0.0,
  "isFlaggedFraud": 0,
  "origin_balance_error": 0.0,
  "destination_balance_error": -181.0,
  "origin_balance_change": 181.0,
  "destination_balance_change": 0.0
}
```

#### 4. Prediction History
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `GET` | `/predictions/history` | Bearer JWT | `USER`, `ANALYST`, `ADMIN` | Get authenticated user's prediction history |

#### 5. Analyst Dashboard
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `GET` | `/analyst/dashboard/stats` | Bearer JWT | `ANALYST`, `ADMIN` | Get total predictions, fraud rates, and avg risk score |
| `GET` | `/analyst/dashboard/risk-distribution` | Bearer JWT | `ANALYST`, `ADMIN` | Get count of predictions per risk level tier |
| `GET` | `/analyst/dashboard/recent-predictions` | Bearer JWT | `ANALYST`, `ADMIN` | Get feed of 10 recent system-wide predictions |

#### 6. Admin Management
| Method | Endpoint | Auth Required | Role | Description |
|---|---|---|---|---|
| `GET` | `/admin/dashboard` | Bearer JWT | `ADMIN` | Admin access status confirmation |
| `GET` | `/admin/users` | Bearer JWT | `ADMIN` | List all registered system users |
| `PATCH` | `/admin/users/{user_id}/role` | Bearer JWT | `ADMIN` | Change target user role (`USER`, `ANALYST`, `ADMIN`) |
| `PATCH` | `/admin/users/{user_id}/status` | Bearer JWT | `ADMIN` | Toggle user active status (`is_active: true/false`) |

---

### FastAPI ML Bridge (Internal ML Microservice)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service health status message |
| `GET` | `/health` | Model status check (`{"status": "healthy", "model_loaded": true}`) |
| `POST` | `/predict` | Internal ML inference endpoint called by Spring Boot |

---

## Authentication & Authorization

- **Token Storage**: Frontend stores JWT in `localStorage` under `finguard_token`.
- **Stateless Verification**: Spring Boot `JwtAuthenticationFilter` validates token signature and checks user active state in PostgreSQL.
- **RBAC Hierarchies**:
  - `USER`: Access to `/predict` and `/predictions/history`.
  - `ANALYST`: `USER` privileges + `/analyst/dashboard/*`.
  - `ADMIN`: Full privileges including `/admin/*` management tools.
- **Self-Protection Enforcement**: System prevents admins from altering their own role or deactivating their own account in `AdminService`.

---

## Database Architecture

- **Production**: **Neon PostgreSQL** managed via Spring Data JPA and Hibernate.
- **Schema Management**: Controlled by `spring.jpa.hibernate.ddl-auto=update`. Tables auto-managed:
  - `users`: Account identities, email, BCrypt password hash, role (`USER`, `ANALYST`, `ADMIN`), active flag.
  - `prediction_audit`: User reference, fraud prediction result, probability, risk score, risk level, recommendation, creation timestamp.
- **Local Fallback**: SQLite connection enabled when `DATABASE_URL` is omitted in development (`jdbc:sqlite:../backend/app/database/finguard.db`).

---

## Admin Bootstrap Mechanism

Spring Boot includes `AdminInitializer` (`com.finguard.springbackend.config.AdminInitializer`).  
On application startup, if environment variables `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` are defined, the system verifies if the account exists. If missing, it creates the initial `ADMIN` account with active status automatically.

---

## Project Structure

```
FinGuard-AI/
├── README.md                           # Comprehensive production documentation
├── pyproject.toml                      # Python ML project metadata
├── paysim.csv                          # PaySim dataset (excluded from VCS)
├── tests/                              # Global test package
│
├── spring-backend/                     # Spring Boot Backend Gateway (Java 17)
│   ├── Dockerfile
│   ├── pom.xml                         # Maven dependencies (Spring Security, JPA, PostgreSQL)
│   └── src/
│       ├── main/
│       │   ├── java/com/finguard/springbackend/
│       │   │   ├── SpringBackendApplication.java
│       │   │   ├── config/             # AdminInitializer, Jackson, Converters
│       │   │   ├── controller/         # Auth, Predict, History, Dashboard, Admin, Health
│       │   │   ├── dto/                # Request & Response DTO records
│       │   │   ├── entity/             # JPA Entities (User, PredictionAudit)
│       │   │   ├── repository/         # Spring Data JPA Repositories
│       │   │   ├── security/           # SecurityConfig, JwtFilter, JwtService, PasswordService
│       │   │   └── service/            # Business services & FastApiClient REST client
│       │   └── resources/
│       │       └── application.properties # Spring application configuration
│       └── test/                       # Spring Boot unit & integration tests
│
├── backend/                            # FastAPI ML Bridge Service (Python 3.11)
│   └── app/
│       ├── main.py                     # FastAPI routes (/health, /predict)
│       ├── schemas.py                  # Pydantic validation models
│       └── services/
│           └── ai_report_generator.py  # Gemini 2.5 Flash report service
│
├── frontend/                           # React + Vite Frontend Application
│   ├── package.json
│   ├── vite.config.js
│   ├── .env                            # Frontend environment configuration
│   └── src/
│       ├── App.jsx                     # Application shell & navigation router
│       ├── App.css / index.css         # Styling system
│       ├── components/                 # React UI components (Login, Admin, Analyst, etc.)
│       └── services/                   # API client layer & JWT helpers
│
└── ml_pipeline/                        # Machine Learning Pipeline Package
    ├── pipeline_runner.py              # ML training orchestrator
    ├── config/                         # ML hyperparameter & path configurations
    ├── data/                           # Data loading, feature engineering, splitting
    ├── preprocessing/                  # ColumnTransformer preprocessor
    ├── training/                       # Classifier trainers (RF, XGB, LGBM, DT, LR)
    ├── explainability/                 # SHAP TreeExplainer & label formatters
    ├── risk/                           # RiskEngine decision matrix
    ├── inference/                      # FraudPredictor inference wrapper
    └── models/                         # Serialized model & preprocessor artifacts (.pkl)
```

---

## Environment Variables

Configure environment variables in your deployment environment or local `.env` files. **Never commit real credentials to version control.**

### Spring Boot Backend Environment Variables
```env
PORT=8080
DATABASE_URL=<neon-postgresql-connection-string>
DB_DRIVER=org.postgresql.Driver
DB_DIALECT=org.hibernate.dialect.PostgreSQLDialect
FASTAPI_URL=<fastapi-service-url>
JWT_SECRET_KEY=<strong-secret-key>
ADMIN_USERNAME=<admin-username>
ADMIN_EMAIL=<admin-email>
ADMIN_PASSWORD=<strong-password>
```

### FastAPI ML Bridge Environment Variables
```env
GEMINI_API_KEY=<google-gemini-api-key>
```

### Frontend Environment Variables
```env
VITE_API_URL=<spring-boot-backend-url>
```

---

## Local Development

### Prerequisites
- Java 17 JDK
- Maven 3.8+ (or included `./mvnw`)
- Python 3.11
- Node.js 18+ & npm

### 1. Setup & Run FastAPI ML Bridge
```bash
cd backend
python -m venv .venv

# Activate Virtual Environment:
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt # or pip install -e ..
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Setup & Run Spring Boot Backend
```bash
cd spring-backend

# Set environment variables for local run if needed
# Runs Spring Boot on http://localhost:8080
./mvnw spring-boot:run
```

### 3. Setup & Run React Frontend
```bash
cd frontend
npm install
npm run dev
```
Access the application at `http://localhost:5173`.

---

## Production Deployment

The project is deployed on **Render** paired with **Neon PostgreSQL**:

- **React Frontend**: Deployed as a Static Site / Web Service.  
  URL: `https://finguard-ai-4ico.onrender.com`
- **Spring Boot Backend**: Deployed as a Java Web Service connecting to Neon PostgreSQL.  
  URL: `https://finguard-ai-spring.onrender.com`
- **FastAPI ML Bridge**: Deployed as a Python Web Service with ML dependencies & Gemini API integration.  
  URL: `https://finguard-ai-backend-60wj.onrender.com`

---

## Security

- **Stateless JWT Security**: Requests signed with HS256 JWT tokens.
- **BCrypt Hashing**: Passwords stored securely using BCrypt encryption.
- **Role-Based Access Control (RBAC)**: Method and endpoint level security via Spring Security.
- **Self-Protection Safeguards**: Server-side prevention of administrative self-demotion or self-deactivation.
- **CORS Policies**: Explicit origin restrictions configured in `SecurityConfig`.
- **Environment Isolation**: All sensitive credentials passed via environment variables.

---

## Testing

- **Backend Context Verification**: Run Spring Boot context and integration tests:
  ```bash
  cd spring-backend
  ./mvnw test
  ```
- **Frontend Production Build**: Verify React application build bundle:
  ```bash
  cd frontend
  npm run build
  ```

---

## Current Status

The core FinGuard AI platform is **fully implemented and operating in production**:
- ✅ Spring Boot REST Gateway & Security Layer active.
- ✅ Neon PostgreSQL persistent data store connected.
- ✅ FastAPI ML Inference Bridge & Gemini AI Reporting active.
- ✅ React SPA Frontend deployed and fully interactive.
- ✅ User Authentication, RBAC, Prediction History, Analyst Dashboard, and Admin Console verified.
