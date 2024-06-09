FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    && apt-get clean

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

CMD ["flask", "run"]
