FROM python:3.12

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

# Copy Pipfile and Pipfile.lock to the container
COPY ["Pipfile", "Pipfile.lock", "./"]

# Explicitly set the Python version for pipenv to use
RUN pipenv --python 3.12 install --dev

# Install gunicorn using pipenv
RUN pipenv install gunicorn

# Copy application files
COPY predict.py lin_reg.bin ./

EXPOSE 9696

# Start the app using gunicorn
ENTRYPOINT ["pipenv", "run", "gunicorn", "--bind=0.0.0.0:9696", "predict:app"]
