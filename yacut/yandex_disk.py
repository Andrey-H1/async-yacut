import aiohttp
import certifi
import ssl

from yacut import app
from yacut.constants import (
    BASE_UPLOAD_PATH, DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL
)

AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


async def upload_file_to_yandex_disk(files):
    """Асинхронная функция загрузки и получения ссылок для скачивания."""
    filenames = []
    download_links = []
    errors = []

    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(
        headers=AUTH_HEADERS,
        connector=connector
    ) as session:

        for file in files:
            filename = file.filename
            if not filename:
                continue

            path_on_disk = BASE_UPLOAD_PATH / filename
            params = {
                'path': path_on_disk.as_posix(),
                'overwrite': 'true'
            }

            try:
                async with session.get(
                    REQUEST_UPLOAD_URL,
                    params=params
                ) as response:

                    response.raise_for_status()
                    data = await response.json()
                    upload_url = data['href']

                async with session.put(
                    upload_url,
                    data=file.stream
                ) as put_response:

                    put_response.raise_for_status()

                download_params = {'path': path_on_disk.as_posix()}
                async with session.get(
                    DOWNLOAD_LINK_URL,
                    params=download_params
                ) as d_response:

                    d_response.raise_for_status()
                    d_data = await d_response.json()
                    final_download_url = d_data['href']

                download_links.append(final_download_url)

                filenames.append(filename)

            except Exception as error:
                user_error = f'Не загружен {filename}. Причина: {str(error)}'
                errors.append(user_error)
                continue

    return filenames, download_links, errors
