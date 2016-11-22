FROM python:2.7
ADD . /opt/bluebolt
WORKDIR /opt/bluebolt
RUN pip install -r requirements.txt
EXPOSE 5001
CMD python main.py