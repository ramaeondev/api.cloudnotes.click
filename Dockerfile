FROM public.ecr.aws/lambda/python:3.11

# Set working directory inside Lambda container
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy application files
COPY ./app ${LAMBDA_TASK_ROOT}/app
COPY requirements.txt .

# Install dependencies in a cached layer
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}" -U --no-cache-dir

# Set the Lambda function handler
CMD ["app.main.handler"]
