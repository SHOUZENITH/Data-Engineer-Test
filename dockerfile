# 1. Start from a lightweight Python base image
FROM python:3.9-slim

# 2. Set the working directory inside the container to /app
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your application code and data into the container
COPY ./solution ./solution
COPY ./data ./data

# 6. Set the command to run when the container starts
CMD ["python", "solution/Solution.py"]