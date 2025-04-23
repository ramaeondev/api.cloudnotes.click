# Cloudnotes API

A FastAPI-based REST API for managing notes and categories with authentication, built to run on AWS Lambda.

## 🚀 Features

- User authentication with JWT tokens
- Note management with categories and attachments
- Email verification and password reset functionality
- AWS Lambda deployment ready
- Multi-region deployment support
- CORS enabled for secure cross-origin requests

## 🛠 Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL with SQLAlchemy ORM
- **Authentication:** JWT with OAuth2
- **Email Service:** Brevo API
- **Deployment:** AWS Lambda via Container Image
- **CI/CD:** GitHub Actions
- **Container:** Docker

## 🏗 Project Structure

```
logit_api/
├── app/
│   ├── core/          # Core configuration
│   ├── db/            # Database models and connection
│   ├── routes/        # API endpoints
│   ├── schemas/       # Pydantic models
│   ├── email_sender.py
│   ├── security.py    # Authentication logic
│   └── main.py        # Application entry point
├── migrations/        # Alembic migrations
├── .github/
│   └── workflows/     # GitHub Actions deployment
└── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker (for deployment)

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/logit_api.git
cd logit_api
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
make run
# or
uvicorn app.main:app --reload
```

## 📝 Environment Variables

Required environment variables:

```
DB_HOST=your_db_host
DB_PORT=your_db_port
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
SECRET_KEY=your_secret_key
BREVO_API_KEY=your_brevo_api_key
FROM_EMAIL=your_sender_email
```

## 🚢 Deployment

The application is configured for deployment to AWS Lambda using GitHub Actions:

1. Set up required AWS resources (Lambda, ECR, API Gateway)
2. Configure GitHub repository secrets
3. Push to master branch or manually trigger workflow

### Required GitHub Secrets

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `ECR_REGISTRY`
- `ECR_REPOSITORY`
- `LAMBDA_FUNCTION_NAME`

## 📚 API Documentation

When running locally, access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔄 Database Migrations

Run migrations using Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "migration_name"

# Apply migrations
alembic upgrade head
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.