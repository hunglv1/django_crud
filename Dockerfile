# Use the official Python image as the base image
FROM python:3.12

# Set environment variables for Python and Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE myproject.settings

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Copy the Django project files to the container
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
