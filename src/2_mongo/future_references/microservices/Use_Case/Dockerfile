FROM tensorflow/tensorflow

RUN apt-get -y update

RUN pip install --upgrade pip

WORKDIR /usr/src/app

RUN mkdir /usr/src/my_share

RUN mkdir /usr/src/get_module

EXPOSE 443 27017 80 9042

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



#CMD ["tail", "-f", "/dev/null"]
CMD ["python3", "DUT_GaN_IMS.py"]
