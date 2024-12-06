# OMS

This project is a backend implementation for an e-commerce platform built using FastAPI, SQLAlchemy, and PostgreSQL. The platform supports functionalities such as user management, order management, product inventory, promotions, and error handling.

## Features

- **User Management**: Create, update, delete users, and retrieve user details.
- **Order Management**: Place, view, cancel orders, and manage order statuses.
- **Product Management**: Add, update, and retrieve product details.
- **Promotions**: Create, update, and apply promotions on products.
- **Concurrency Handling**: Prevent race conditions when updating product stock.
- **Pagination and Filtering**: Support pagination and filtering for products and orders.
- **Error Handling**: Handle errors like insufficient stock, invalid orders, and unauthorized access.

## Setup

### Prerequisites

1. **Docker**: Ensure you have Docker installed to easily manage containers and run the application.
2. **Docker Compose**: Used to manage multi-container Docker applications (like PostgreSQL and FastAPI).
3. **Python 3.9+**: For local testing (optional if using Docker).
4. **PostgreSQL**: A PostgreSQL database is required for this project. Docker will automatically spin up the database.

### Running the Application Using Docker

This project uses Docker and Docker Compose for containerization. Follow the steps below to get the application running.

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository

run:
docker-compose up --build

stop:
docker-compose down

test:
http://localhost:8000/docs



