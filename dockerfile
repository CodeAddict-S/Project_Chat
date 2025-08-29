FROM python:3.12-slim
WORKDIR /home/samir4556/Projects/project_chat
COPY . .
RUN pip install -r requirements.txt
CMD ["daphne", "core.asgi:application"]