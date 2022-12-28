FROM python:3-slim
#alpine

WORKDIR /usr/src/app

COPY ./requirements.txt ./
#COPY ./hostlist.txt ./
#COPY ./urllist.txt ./

RUN mkdir -p /mnt/config
COPY /*.cfg  /mnt/config/
 
RUN pip install --no-cache-dir -r requirements.txt
COPY ./main.py /usr/src/app/main.py

CMD ["python","-u","main.py"]
