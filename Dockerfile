# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Install nmap
RUN apt-get update && \
    apt-get install -y nmap \
    wget \
    curl \
    libmaxminddb0 \
    libmaxminddb-dev \
    mmdb-bin && \
    rm -rf /var/lib/apt/lists/*

ARG MAXMIND_ACCOUNT_ID
ARG MAXMIND_LICENSE_KEY

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt



# Download the MaxMind GeoLite2 ASN database

RUN curl -O -J -L -u ${MAXMIND_ACCOUNT_ID}:${MAXMIND_LICENSE_KEY} 'https://download.maxmind.com/geoip/databases/GeoLite2-ASN/download?suffix=tar.gz' &&\
    mkdir -p /usr/local/share/GeoIP && \
    tar --strip-components=1 -xzf GeoLite2-ASN_20240803.tar.gz -C /usr/local/share/GeoIP && \
    rm GeoLite2-ASN_20240803.tar.gz

# Download the MaxMind GeoLite2 Citys database

RUN curl -O -J -L -u ${MAXMIND_ACCOUNT_ID}:${MAXMIND_LICENSE_KEY} 'https://download.maxmind.com/geoip/databases/GeoLite2-City/download?suffix=tar.gz' &&\
    mkdir -p /usr/local/share/GeoIP && \
    tar --strip-components=1 -xzf GeoLite2-City_20240730.tar.gz -C /usr/local/share/GeoIP && \
    rm GeoLite2-City_20240730.tar.gz


# Copy the project code into the container
COPY . /app/

# Expose the port that the Django app runs on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
