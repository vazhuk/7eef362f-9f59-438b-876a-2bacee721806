FROM python:3.8-alpine

WORKDIR /app

COPY . .
RUN pip3 install flask httpx asyncio redis cachetools

CMD [ "python3", "-m" , "invoker"]