set -e

IMAGE_NAME="data-solution"

echo "--- Building the Docker image ($IMAGE_NAME)... ---"
docker build -t $IMAGE_NAME .

echo ""
echo "--- Running the Docker container... ---"
docker run --rm $IMAGE_NAME