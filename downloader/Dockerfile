FROM python
COPY requirements.txt /parser/requirements.txt
WORKDIR /parser
RUN pip install -r requirements.txt
COPY . /parser


CMD ["python", "main.py"]

