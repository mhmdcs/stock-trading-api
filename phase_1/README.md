# PHASE ONE (Getting to know FastAPI)

![phase_one](../imgs/phase-one.jpg)

## Technology used

- WEB SERVER - [FastAPI](https://fastapi.tiangolo.com/)
- ORM - [SQLAlchemy](https://fastapi.tiangolo.com/advanced/async-sql-databases/?h=sqlalchemy#import-and-set-up-sqlalchemy)
- DATABASE -  [cockroachdb](https://www.cockroachlabs.com/)
- Scheme Validation - [Pydantic](https://fastapi.tiangolo.com/tutorial/body-nested-models/)

## Objectives

Build a `FASTAPI` server that retrieve the latest stock market prices from and external resource [Rapid API](https://rapidapi.com/twelvedata/api/twelve-data1) and give the user the ability to manage a custom alert rules by preissiting them in a database so they can crate/update/delete/read thier rules

## Functionality

> 🚨 please don't waste some time to build and Authentication/Authorization functionality

- **Retrieve the latest market prices**
  - returns stock prices for the following symbols
    - AAPL
    - MSFT
    - GOOG
    - AMZN
    - META
- **Create alert rule**
  - alerts have the following properties
    - name
    - threshold price
    - symbol
- **Delete alert rule**
- **Get alerts rules**
- **Update alerts rules**

## Routes and Descriptions

- `GET /market-prices`
  - Returns the latest market prices for mentioned symbols.
- `POST /alert-rules`
  - Creates an alert rule with the following properties: name, threshold price, and symbol.
- `PATCH /alert-rules/{id}`
  - Update an alert rule by ID.
- `DELETE /alert-rules/{id}`
  - Deletes an alert rule by ID.
- `GET /alert-rules`
  - Returns all alert rules.
- `GET /alerts`
  - Returns all alerts.

## TASKS Breakdown

> 📢📢📢 if you're having issues with imports for example `ModuleNotFoundError: No module named 'api' , make sure to add investor_bulletin path in PYTHONPATH, e.g. `export PYTHONPATH="$(pwd)/investor_bulletin" && python investor_bulletin/api/main.py - please check this article https://www.devdungeon.com/content/python-import-syspath-and-pythonpath-tutorial`

- [ ] **Set up your environment**
 Whether on your machine or using docker, make sure you have an updated python version min `3.11` and a running a cockroachdb DB server
--
- [ ] **Create your web server**
--
- [ ] **Create an account and subscribe to Twelvedata API**
Twelvedata API is one of the multiple stock related APIs from [Rapid API](https://rapidapi.com/twelvedata/api/twelve-data1) - `💡 You can choose dif-ferent source API to retrieve the market data`
--
- [ ] **Create your first endpoint to retrieve market data**
Required symbols/tickers `AAPL,MSFT,GOOG,AMZN,META`
--
- [ ] **Use Pydantic to validate user inputs and server responses**
--
- [ ] **Setup your ORM models (RuleAlerts, Alerts) and connect them with the DB server**
alerts should have the following properties `name, threshold price, symbol`
--
- [ ] **Create a CRUD API for users to manage the alert rules**
--
- [ ] **Seed the alerts table with data**
--
- [ ] **Create an API to fetch alerts**
--
- [ ] **Apply separation of concern by segregating your logic following the `investor_bulletin folder` structure there is already commented code to guid you through**

## What's next

- **If you complete the tasks**, just send an email with the a link of your work in your github, tell us more about your comfort level out of 5 and what was the most challenging part and the most rewarding part.
--

- **If you stuck, or it took so long*- it ok, we understand just send an email with the a link of your work in your github, tell us more about your comfort level out of 5 and how much did you actually completed from the task out of 7, where are you stuck or what took the most of your time
