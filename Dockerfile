# Pull base image
FROM python:3.10.9

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Needed for bitcoinlib package
RUN apt-get update && apt-get install --no-install-recommends -y libgmp-dev

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/
