FROM python:3.6.7
ADD ./lianjia   /code
ADD ./scrapyd.conf   /code
ADD ./requirements.txt   /code
ADD ./google-chrome-stable_current_amd64.deb   /code
WORKDIR /code
COPY ./scrapyd.conf /etc/scrapyd/
EXPOSE 6800
#安装chromedriver
RUN apt-get update && apt-get install zip -y
RUN wget http://npm.taobao.org/mirrors/chromedriver/72.0.3626.7/chromedriver_linux64.zip
RUN unzip -d /usr/bin chromedriver_linux64.zip
#安装chrome
RUN dpkg -i google-chrome*; apt-get -f install -y
RUN pip install -r requirements.txt
CMD scrapyd
