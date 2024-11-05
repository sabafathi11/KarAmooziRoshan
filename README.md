# Dataset Labeling Project

## Overview

Dataset Labeling Project is a Django application that allows for dataset labeling and management. Each dataset in the
system includes labels and texts, and users can label texts with any label associated with the dataset the text belongs
to. The project supports Docker for deployment, CSV file import for dataset creation, and automatic daily reports of
user activities.

## Features

* User(Operator), Dataset, Label, and Text models for structured dataset management
* ActivityLog and Report models for tracking users' actions.
* Labeling System: Each text can be labeled using labels associated with its dataset
* JWT for authentication
* Permission handling for datasets
* CSV Import: Bulk import datasets via CSV files
* Automated Daily Reports: Daily activity reports saved in database Report model
* Dockerized: Easy setup with Docker
* PostgreSQL as the database

## Prerequisites

* Python (>= 3.12 recommended)
* Docker and Docker Compose
* PostgreSQL

## API Endpoints

Below is a list of the API routes for the Dataset Labeling Project.

### Authentication

| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| POST   | `/accounts/register/` | register for users |
| POST   | `/accounts/login/`    | login for users    |

There is also a `/accounts/users/` router for all CRUD requests that is only accessible for admin.

### Dataset Management

To access datasets you should be creator of it or the accessibility should have been granted to you. Since the
authentication flow is implemented with JWT, you need to have access token in your headings to have access to following
endpoints.

Labels can be created nested inside datasets.

| Method | Endpoint                | Description                 |
|--------|-------------------------|-----------------------------|
| GET    | `/data/datasets/`       | List all datasets           |
| POST   | `/data/datasets/`       | Create a new dataset        |
| GET    | `/data/datasets/<id>/`  | Retrieve a specific dataset |
| PUT    | `/data/datasets/<id>/`  | Update a specific dataset   |
| DELETE | `/data/datasets/<id>/`  | Delete a specific dataset   |
| POST   | `/datasets/import-csv/` | Import a dataset via CSV    |

### Label Management

I recommend to create and update labels inside dataset routers. So that you wouldn't conflict same label names that
belong to different datasets.

| Method | Endpoint             | Description               |
|--------|----------------------|---------------------------|
| GET    | `/data/labels/`      | List all labels           |
| POST   | `/data/labels/`      | Create a new label        |
| GET    | `/data/labels/<id>/` | Retrieve a specific label |
| PUT    | `/data/labels/<id>/` | Update a specific label   |
| DELETE | `/data/labels/<id>/` | Delete a specific label   |

### Text Management

| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| GET    | `/data/texts/`      | List all texts           |
| POST   | `/data/texts/`      | Create a new text        |
| GET    | `/data/texts/<id>/` | Retrieve a specific text |
| PUT    | `/data/texts/<id>/` | Update a specific text   |
| DELETE | `/data/texts/<id>/` | Delete a specific text   |

### Reporting and Actions
This endpoint is only accessible with admin user Authenticated.

| Method | Endpoint             | Description                            |
|--------|----------------------|----------------------------------------|
| GET    | `/accounts/reports/` | List all reports with their activities |


## Additional Notes

* There are some json files in KarAmooziRoshan\docs\json data folder you can use for POST endpoints.
* Each text can have multiple labels.
* If you are importing csv file for creating dataset, and you want to have multiple labels, use '/' between labels.
* File format is checked. So if you import files that don't have .csv extension you will get error.
* Docker and Celery part were added to project in final step and due to time limit were not debugged completely.
