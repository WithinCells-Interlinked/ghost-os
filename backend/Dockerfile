# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install uv, the Python package manager
RUN pip install uv

# Copy the requirements file into the container at /usr/src/app
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Run uvicorn when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
