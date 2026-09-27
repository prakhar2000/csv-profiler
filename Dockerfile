FROM python:3.12-slim

WORKDIR /app
COPY profile.py /app/profile.py
RUN mkdir -p /inputs /outputs

ENTRYPOINT ["python", "/app/profile.py"]
