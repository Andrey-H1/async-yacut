from pathlib import Path
import string


ORIGINAL_URL_LENGTH = 2048
SHORT_URL_LENGTH = 16
MIN_LENGTH = 1
AUTO_URL_LENGTH = 6
AUTO_ALLOWED_CHARS = string.ascii_letters + string.digits
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
BASE_UPLOAD_PATH = Path('/Приложения/Uploader')
