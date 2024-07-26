FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    build-essential \
    python3-pip \
    python3-dev \
    cmake \
    libopenmpi-dev \
    zlib1g-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy all files to /workspace
COPY . /workspace

# Set working directory
WORKDIR /workspace

# Run the Python script to install requirements
RUN pip install --no-cache-dir -r requirements-dev.txt \
    && pip install jupyter

# Clean up unnecessary packages
RUN apt-get purge -y \
    build-essential \
    cmake \
    libopenmpi-dev \
    zlib1g-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["bash"]