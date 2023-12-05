FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["sh", "-c", "streamlit run --server.address=$STREAMLIT_SERVER_ADDRESS --server.port=$STREAMLIT_PORT ui.py"]
