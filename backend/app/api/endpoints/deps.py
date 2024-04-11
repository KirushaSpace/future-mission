from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from app.utils.minio_client import MinioClient


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/login/access-token"
)


def minio_auth() -> MinioClient:
    minio_client = MinioClient(
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        bucket_name=settings.MINIO_BUCKET,
        minio_url=settings.MINIO_URL,
    )
    return minio_client