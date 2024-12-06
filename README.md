# Order Management System

This project implements a set of CRUD operations for managing users, orders, and products in an e-commerce system using FastAPI and SQLAlchemy.

## Table of Contents
- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
  - [User Endpoints](#user-endpoints)
  - [Order Endpoints](#order-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
- [Explanation of Code](#explanation-of-code)
  - [CRUD Operations](#crud-operations)
  - [Order Management](#order-management)
  - [Authentication](#authentication)
- [License](#license)

## Project Overview

This project provides an API for managing users, products, orders, and promotions in an e-commerce platform. The backend is built using FastAPI, and it uses SQLAlchemy for ORM (Object-Relational Mapping) with a PostgreSQL database.

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

```start
docker-compose up --build

```stop and remove
docker-compose down

```test
http://localhost:8000/docs



