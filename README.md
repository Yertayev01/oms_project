# Order Management System

This project implements a set of CRUD operations for managing users, orders, and products in an e-commerce system using FastAPI and SQLAlchemy.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#docker-commands)

## Project Overview

This project provides an API for managing users, products, orders in a platform. The backend is built using FastAPI, and it uses SQLAlchemy for ORM (Object-Relational Mapping) with a PostgreSQL database.

## Technologies Used
- **FastAPI**: Modern web framework for building APIs.
- **SQLAlchemy**: ORM for database management.
- **PostgreSQL**: Database for storing data.
- **Pydantic**: Data validation and settings management.
- **JWT**: JSON Web Tokens for authentication.
- **Python**: Main programming language.

## Setup and Installation

Follow these steps to set up and run the project locally:

### Prerequisites
- Python 3.8+
- PostgreSQL Database
- Docker (optional, for containerization)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Yertayev01/oms_project.git
   cd oms_project

## Docker Commands

### To Run the Application:
docker-compose up --build

### To Stop And Remove:
docker-compose down

### Test Swagger Documentation:
http://localhost:8000/docs



