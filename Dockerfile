# Python ka base image use karo
FROM python:3.9

# Folder set karo
WORKDIR /code

# Requirements copy karke install karo
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Pura code copy karo
COPY . /code

# Permission set karo (Hugging Face ke liye zaroori hai)
RUN chmod -R 777 /code

# Server start karo (Hugging Face port 7860 use karta hai)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]