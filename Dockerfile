
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/      ./apps/
COPY common/    ./common/
COPY data/      ./data/
COPY static/    ./static/
COPY templates/ ./templates/
COPY LICENSE    .
COPY run.py     .

EXPOSE 1337

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=1337"]

