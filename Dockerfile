FROM python:3.13-slim

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

CMD ["python", "-m", "app.main"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
CMD pgrep -f "python.*app.main" || exit 1