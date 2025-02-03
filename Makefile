.PHONY: all

# Variables
IMAGE_NAME = mm-token-counter-image
CONTAINER_NAME = mm-token-counter-container
# Set to the current directory (root of the project)
OUTPUT_DIR =.

all: build run

clean: clean-all

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run: stop-container
	docker run --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop and remove the existing container if it exists
stop-container:
	@if [ "$(shell docker ps -aq -f name=$(CONTAINER_NAME))" ]; then \
		docker rm -f $(CONTAINER_NAME); \
	fi

# Copy the PDF from the container to the host
copy-context:
	docker cp $(CONTAINER_NAME):/app/context.txt $(OUTPUT_DIR)/context.txt

# Clean up the Docker container
clean-container:
	docker rm -f $(CONTAINER_NAME)

# Clean up the Docker image
clean-image:
	docker rmi $(IMAGE_NAME)

# Delete all docker volumes, images, and containers
clean-all:
	docker system prune -a
	docker volume prune
	docker image prune
	docker container prune
