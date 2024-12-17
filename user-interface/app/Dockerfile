FROM python:3.11

WORKDIR /app

COPY requirements_demo.txt ./
COPY simpleChat.py ./

RUN pip install --upgrade pip
RUN pip install -r requirements_demo.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "simpleChat.py", "--server.port=8501", "--server.address=0.0.0.0"]
