FROM MySQL

RUN apt-get update
RUN apt-get install python3

COPY .

RUN python3 pip wswolf/requirements.txt