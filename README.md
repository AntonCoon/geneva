# GenEvA

GenEvA (**Gen**e **Ev**idence **A**pp) is a web application that explores potential correlations between genes and diseases using public life sciences data and LLM analysis.  

## Features
- Query gene-disease associations via a web interface  
- Provides structured JSON output for downstream applications  
- Easy setup with Docker  

## Setup & Running
**Step 1: Clone the repository**  
```bash
git clone https://github.com/AntonCoon/geneva.git
cd geneva
```
**Step 2: Run with Docker Compose**  
```bash
sudo docker compose up
```
**Step 3: Access the app**  
Open your browser at: `http://127.0.0.1:8000/app`
API documentation is available at: `http://127.0.0.1:8000/docs`

## Technical Stack & Decisions

- **FastAPI**: Lightweight framework with automatic API docs and async support.  
  - *Alternative*: Django for a full-featured framework with built-in admin, authentication, and migrations; Flask for minimalistic flexibility.  
  - *Trade-off*: FastAPI is ideal for small/demo APIs, but Django or Flask might be better for complex applications with built-in tools.  

- **SQLModel**: Combines Pydantic models with async-friendly ORM, simple syntax.  
  - *Alternative*: SQLAlchemy with Alembic for robust schema migrations and advanced ORM features; Tortoise ORM for async support.  
  - *Trade-off*: SQLModel is lightweight and easy to use, but SQLAlchemy provides more control and production-grade migration capabilities.  

- **Docker Compose**: Ensures consistent environment setup across machines.  
  - *Alternative*: Kubernetes for scalable production deployments, or virtual environments for local development.  
  - *Trade-off*: Docker Compose is perfect for local/demo use; production systems may need orchestration, monitoring, and logging.  

- **Trade-offs Summary**:  
  - Current setup is optimized for local/demo use. Scaling for production would require:  
    - Using a production-grade database (PostgreSQL, MySQL) instead of SQLite  
    - Production deployment (Kubernetes, Docker Swarm)  
    - Adding authentication, monitoring, and logging  
    - Possibly separating backend and frontend for better scalability and maintainability


## Future Improvements

- **User authentication & authorization**: Implement secure login and access control.  
- **Caching**: Use LRU cache or Redis for in-memory caching to speed up repeated queries.  
- **Large-scale dataset support**: Optimize data handling and queries for scalability.  
- **Logging & monitoring**: Add structured logging, error handling, and monitoring dashboards (e.g., Grafana, Prometheus).  
- **Frontend/backend separation**: Decouple the frontend from the backend for better maintainability and scalability.  
- **Improved exception handling**: Graceful error responses and better debugging support.  
