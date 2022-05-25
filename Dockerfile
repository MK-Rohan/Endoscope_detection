# syntax=docker/dockerfile:1

FROM python:3.9.7

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

# WORKDIR /pylori_analysis

# COPY requirements.txt requirements.txt

# RUN pip3 install -r requirements.txt

# COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]