# FastAPI Project

This is a FastAPI project. Follow the steps below to set up and run the project locally.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Steps to Run the Project

1. **Clone the Repository**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   ```
3. **Activate the Virtual Environment**
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
        - On macOS/Linux:
          ```bash
          source venv/bin/activate
          ```
4. **Install Dependencies**
5. ```bash
   pip install -r requirements.txt
   ```
6. **Run the FastAPI Application**
   ```bash
   uvicorn fast-api:app --host 0.0.0.0 --port 8000
   ```
    - Here, `fast-api` is the name of your Python file (without the `.py` extension) and `app` is the name of the
      FastAPI instance.
7. **Access the Application**
    - your server should now be running at `http://localhost:8000`
    - You can access the automatic interactive API documentation at `http://localhost:8000/docs` or
      `http://localhost:8000/redoc`

## Additional Notes

- Make sure to deactivate the virtual environment when you're done:
  ```bash
  deactivate
  ```