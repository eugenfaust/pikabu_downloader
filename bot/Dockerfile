FROM python
COPY requirements.txt /bot/requirements.txt
WORKDIR /bot
RUN pip install -r requirements.txt
COPY . /bot


CMD ["python", "polling.py"]

