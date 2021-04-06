FROM python:3.7-slim
WORKDIR /app
COPY ./ /app/
RUN apt-get update && apt-get install -y python3-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get remove --purge -y python3-dev
RUN apt-get -y clean
EXPOSE 5000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "--workers", "4", "main:app"]
