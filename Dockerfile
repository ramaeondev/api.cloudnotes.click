FROM public.ecr.aws/lambda/python:3.11

# Set working directory inside Lambda container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy application files
COPY ./app ${LAMBDA_TASK_ROOT}/app
COPY requirements.txt .

# Install dependencies
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" -U --no-cache-dir

# Set the correct handler (adjust based on your structure)
CMD ["app.main.handler"]