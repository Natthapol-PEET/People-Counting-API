FROM python:3

COPY src /src/app
WORKDIR /src/app

# create env
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# timezone env with default
ENV TZ Asia/Bangkok

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies:
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Run the application:
CMD ["python", "app.py"]
