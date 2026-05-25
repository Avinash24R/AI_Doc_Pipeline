import os


class Settings:

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://admin:password@postgres:5432/document_pipeline"
    )

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )

    UPLOAD_DIR = "app/uploads"

    SMTP_HOST = os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 2525))

    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")


settings = Settings()