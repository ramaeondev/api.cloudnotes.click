# Use the AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Set the working directory to Lambda's expected location
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Set the Lambda handler
CMD ["app.main.handler"]