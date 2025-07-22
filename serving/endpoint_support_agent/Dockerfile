# Use an official Python runtime as a parent image
FROM us-central1-docker.pkg.dev/thermal-effort-466412-a6/custom-image-repository/base_image:base_image_1.0.0

# Set the working directory in the container
WORKDIR /opt/app

# Copy the current directory contents into the container
COPY . .

# Install the dependencies
RUN pip install --no-deps -e .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "support_agent:app", "--host", "0.0.0.0", "--port", "8000"]