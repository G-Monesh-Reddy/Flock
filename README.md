# Flock Energy Assignment

## REST API Wrapper for Urja Meter Ops

### Overview

This project implements a REST API wrapper around the legacy **Urja Meter Ops** web application. The service automates authentication, manages user sessions, retrieves smart meter information from the legacy portal, parses HTML responses into structured JSON, and exposes clean REST endpoints for downstream applications.

The project is built using **Python**, **FastAPI**, **Requests**, and **BeautifulSoup**.

---

## Features

* Session-based authentication with the legacy portal
* Automatic session persistence using cookies
* Automatic re-authentication when the session expires
* HTML parsing and data normalization
* Clean REST API endpoints
* Auto-generated Swagger/OpenAPI documentation
* Health check endpoint

---

## Technology Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Requests
* BeautifulSoup4
* lxml

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd flock-energy-assignment
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the server:

```bash
uvicorn main:app --reload
```

The server will be available at:

```
http://localhost:8000
```

---

## API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

OpenAPI Specification

```
http://localhost:8000/openapi.json
```

---

## API Endpoints

### Home

```
GET /
```

Returns service information.

---

### Login

```
GET /login
```

Authenticates with the legacy portal.

---

### List Smart Meters

```
GET /meters
```

Returns all available smart meters.

Example Response

```json
[
  {
    "meter_id": "1001",
    "consumer": "John Doe",
    "status": "Active",
    "location": "Hyderabad"
  }
]
```

---

### Meter Details

```
GET /meters/{meter_id}
```

Returns detailed information for a specific smart meter.

---

### Consumption History

```
GET /meters/{meter_id}/consumption
```

Returns historical consumption data.

Example Response

```json
[
  {
    "date": "2026-07-01",
    "consumption": 145.6
  }
]
```

---

### Network Tree

```
GET /network-tree
```

Returns the organizational/network hierarchy (if supported by the legacy portal).

---

### Health Check

```
GET /health
```

Example Response

```json
{
  "status": "UP"
}
```

---

## Project Structure

```
.
├── main.py
├── requirements.txt
├── README.md
└── REFLECTION.md
```

---

## Configuration

Update the following constants in `main.py` before running the application:

* BASE_URL
* LOGIN_URL
* METERS_URL
* USERNAME
* PASSWORD

Also update the HTML parsing selectors to match the actual structure of the Urja Meter Ops portal.

---

## Architecture

The application follows a simple layered architecture:

1. **Legacy Client Layer**

   * Handles login
   * Maintains session cookies
   * Sends authenticated requests
   * Automatically re-authenticates when required

2. **Parser Layer**

   * Parses HTML responses
   * Cleans and normalizes data
   * Converts HTML tables into structured JSON

3. **REST API Layer**

   * Exposes clean REST endpoints
   * Returns standardized JSON responses
   * Automatically generates OpenAPI documentation

---

## Design Decisions

* FastAPI was selected because it automatically generates OpenAPI documentation.
* Requests Session is used to persist cookies across multiple requests.
* BeautifulSoup simplifies parsing HTML tables returned by the legacy portal.
* Thread locking prevents multiple simultaneous login requests.

---

## Assumptions

* The legacy application uses session-based authentication.
* HTML pages contain predictable table structures.
* Authentication credentials are valid.
* Internet connectivity is available while accessing the portal.

---

## Future Improvements

* Environment variable support using `.env`
* Structured logging
* Redis-based session caching
* Async HTTP client (`httpx`)
* Retry mechanism for transient failures
* Unit and integration tests
* Docker containerization
* CI/CD pipeline using GitHub Actions

---

## Sample cURL Requests

Get all meters

```bash
curl http://localhost:8000/meters
```

Get meter details

```bash
curl http://localhost:8000/meters/1001
```

Get consumption history

```bash
curl http://localhost:8000/meters/1001/consumption
```

Health check

```bash
curl http://localhost:8000/health
```

---

## Author

Developed as part of the **Flock Energy Backend Assignment** using Python and FastAPI.
