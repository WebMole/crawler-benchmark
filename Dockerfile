FROM python:2.7-jessie

RUN apt-get update -y \
	&& apt-get install -y \
		build-essential \
		python-dev \
		g++ \
		libfreetype6-dev \
		build-essential \
		libpng-dev \
		libjpeg62-turbo-dev \
		python-matplotlib \
		libffi-dev \
		postgresql \
		postgresql-client \
	&& apt-get clean \
	&& rm -rf /var/cache/apt/archives/* /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN easy_install -U distribute

WORKDIR /app

ADD ./requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

EXPOSE 8080

CMD python runserver.py