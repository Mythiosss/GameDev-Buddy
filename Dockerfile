FROM ollama/ollama:latest AS ollama
FROM python:3.12-slim

WORKDIR /app

COPY --from=ollama /usr/bin/ollama /usr/bin/ollama
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend
COPY start.sh ./start.sh
RUN chmod +x ./start.sh

ENV PORT=8000
ENV OLLAMA_HOST=http://127.0.0.1:11434
ENV OLLAMA_MODEL=gemma3:4b
EXPOSE 8000

ENTRYPOINT ["/app/start.sh"]
