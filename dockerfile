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
    && rm -rf /var/index/lib/apt/lists/*

COPY requirements.txt /workspace/requirements.txt

RUN pip install --no-cache-dir -r /workspace/requirements-dev.txt

COPY . /workspace

RUN pip install jupyter

RUN apt-get purge -y \
    build-essential \
    cmake \
    libopenmpi-dev \
    zlib1g-dev \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["jupyter", "notebook", "--ip='0.0.0.0'", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--Notebookup.password=''"]

EXPOSE 8888
