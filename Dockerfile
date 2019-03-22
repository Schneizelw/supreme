FROM python:3.6.7
ADD ./lianjia   /code
ADD ./scrapyd.conf   /code
ADD ./chromedriver   /code
ADD ./requirements.txt   /code
WORKDIR /code
COPY ./scrapyd.conf /etc/scrapyd/
COPY ./chromedriver /usr/bin/
EXPOSE 6800
RUN pip install -r requirements.txt
CMD scrapyd
