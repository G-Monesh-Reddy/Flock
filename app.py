from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import threading

app = FastAPI(
    title="Flock Energy Assignment",
    version="1.0",
    description="REST API Wrapper around Urja Meter Ops"
)

# -----------------------------
# CONFIG
# -----------------------------

BASE_URL = "https://your-urja-portal.com"

LOGIN_URL = BASE_URL + "/login"

METERS_URL = BASE_URL + "/meters"

USERNAME = "YOUR_USERNAME"

PASSWORD = "YOUR_PASSWORD"

session = requests.Session()

lock = threading.Lock()

logged_in = False


# -----------------------------
# LOGIN
# -----------------------------

def login():

    global logged_in

    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }

    response = session.post(LOGIN_URL, data=payload)

    if response.status_code != 200:
        raise Exception("Login Failed")

    logged_in = True


def ensure_login():

    global logged_in

    with lock:

        if not logged_in:
            login()


# -----------------------------
# REQUEST WRAPPER
# -----------------------------

def get(url):

    ensure_login()

    response = session.get(url)

    if response.status_code == 401:

        login()

        response = session.get(url)

    return response


# -----------------------------
# HTML PARSER
# -----------------------------

def parse_meter_table(html):

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")

    if table is None:
        return []

    rows = table.find_all("tr")

    data = []

    for row in rows[1:]:

        cols = row.find_all("td")

        if len(cols) == 0:
            continue

        item = {}

        item["meter_id"] = cols[0].text.strip()

        item["consumer"] = cols[1].text.strip()

        item["status"] = cols[2].text.strip()

        item["location"] = cols[3].text.strip()

        data.append(item)

    return data


# -----------------------------
# API
# -----------------------------

@app.get("/login")
def api_login():

    try:

        login()

        return {
            "message": "Login Successful"
        }

    except Exception:

        raise HTTPException(500, "Login Failed")


@app.get("/meters")
def meters():

    response = get(METERS_URL)

    data = parse_meter_table(response.text)

    return data


@app.get("/meters/{meter_id}")
def meter_details(meter_id: str):

    url = f"{BASE_URL}/meter/{meter_id}"

    response = get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    details = {}

    labels = soup.find_all("label")

    values = soup.find_all("span")

    for l, v in zip(labels, values):
        details[l.text.strip()] = v.text.strip()

    return details


@app.get("/meters/{meter_id}/consumption")
def consumption(meter_id: str):

    url = f"{BASE_URL}/meter/{meter_id}/consumption"

    response = get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table")

    if table is None:
        return []

    rows = table.find_all("tr")

    result = []

    for row in rows[1:]:

        cols = row.find_all("td")

        if len(cols) < 2:
            continue

        result.append({
            "date": cols[0].text.strip(),
            "consumption": float(cols[1].text.strip())
        })

    return result


@app.get("/network-tree")
def network_tree():

    url = BASE_URL + "/network"

    response = get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    nodes = []

    for li in soup.find_all("li"):

        nodes.append(li.text.strip())

    return nodes


@app.get("/")
def home():

    return {
        "message": "Flock Energy REST API Wrapper"
    }


@app.get("/health")
def health():

    return {
        "status": "UP"
    }