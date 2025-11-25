FROM python:3.13-slim

RUN pip install --upgrade pip

#set the working dir
WORKDIR /root/ml/end-to-end_ML

ENV PYTHONPATH=/root/ml/end-to-end_ML


COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "app:application", "--host", "0.0.0.0", "--port", "8000"]


