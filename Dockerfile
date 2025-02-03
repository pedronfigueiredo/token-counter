FROM python:3.13.1-slim-bullseye@sha256:9bf6829d24e9304305ec87973c3b73a94a347019ce0b21994eeb5101dba7c08e

# Docker image name and container name
LABEL name="mm-token-counter-image"
LABEL container_name="mm-token-counter-container"

# Set the working directory inside the container
WORKDIR /app

# Install Git (and any other system dependencies)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install the required Python package for token counting
RUN pip install tiktoken

# Clone the metamask-extension repository via HTTPS
RUN git clone https://github.com/MetaMask/metamask-extension.git --depth 1

# Copy the repository preparation script into the container and ensure it's executable
COPY scripts/prepare_repository.py /app/prepare_repository.py
RUN chmod +x /app/prepare_repository.py

# Copy the token counting script into the container and ensure it's executable
COPY scripts/count_tokens.py /app/count_tokens.py
RUN chmod +x /app/count_tokens.py

# Delete context.txt if it exists
RUN rm -f /app/context.txt

# Set the default command to first prepare the repository (which may generate context.txt)
# and then count the tokens in context.txt using o200k_base encoding.
CMD ["/bin/sh", "-c", "/app/prepare_repository.py && python /app/count_tokens.py --file /app/context.txt --encoding o200k_base"]