FROM bitnami/python
RUN mkdir /src
WORKDIR /src
COPY . /src
RUN pip install -r requirements.txt
