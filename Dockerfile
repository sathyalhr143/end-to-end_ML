    # FROM python:3.13-slim

# RUN pip install --upgrade pip

# #set the working dir
# WORKDIR /root/ml/end-to-end_ML

# ENV PYTHONPATH=/root/ml/end-to-end_ML


# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt


# EXPOSE 8000

# CMD ["uvicorn", "app:application", "--host", "0.0.0.0", "--port", "8000"]


        # 1. Use an official Python runtime
FROM python:3.13-slim

# 2. Set the working directory  
WORKDIR /app

# 3. CRITICAL STEP: Install system build tools
# ML libraries often need these to compile
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy code to the container
COPY . .

# 5. Upgrade pip first (helps avoid installation errors)
RUN pip install --upgrade pip

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Expose the port (Change 8501 to whatever your app uses)
EXPOSE 8000

# 8. Command to run the app
# CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

    CMD ["uvicorn", "app:application", "--host", "0.0.0.0", "--port", "8000"]