FROM python:3.9-slim
LABEL maintainer="stevenbetancurt@hotmail.com"

# Set the working directory to /app
WORKDIR /app

# We copy files
ADD ./src /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "melisa.py"]

# docker build -t stevensotelo/melisafb:latest .
# docker run --name melisa_fb -p 4000:80  stevensotelo/melisafb:latest

# docker tag 02ec98fbd430 stevensotelo/melisafb:latest
# docker push stevensotelo/melisafb:latest