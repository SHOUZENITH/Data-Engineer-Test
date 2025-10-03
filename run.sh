#!/bin/bash

# This line ensures the script will exit immediately if any command fails
set -e

# Define a name for our Docker image
IMAGE_NAME="data-solution"

echo "--- Building the Docker image ($IMAGE_NAME)... ---"
# Build the image using the Dockerfile in the current directory (.)
docker build -t $IMAGE_NAME .

echo ""
echo "--- Running the Docker container... ---"
# Run the container from the image we just built
# The --rm flag automatically removes the container when it exits
docker run --rm $IMAGE_NAME