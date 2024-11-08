FROM python:3.10-slim

COPY main.py requirements.txt ./
RUN python3 -m pip install --break-system-packages -r requirements.txt

ENTRYPOINT ["python3", "main.py"]