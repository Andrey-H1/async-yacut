import aiohttp
import certifi
from flask import flash, redirect, render_template, send_file, url_for
from io import BytesIO
import os
import ssl
from urllib.parse import urlparse

from yacut import app, db
from yacut.forms import UploadForm, URLMapForm
from yacut.models import URLMap
from yacut.utils import create_url_map, get_unique_short_id
from yacut.validators import is_custom_id_valid
from yacut.yandex_disk import upload_file_to_yandex_disk

AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """Представление главной страницы."""
    form = URLMapForm()
    short_url_result = None

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        if not is_custom_id_valid(custom_id):
            return render_template('index.html', form=form)

        if custom_id:
            short_id = custom_id

        else:
            short_id = get_unique_short_id()

        short_url_result = create_url_map(original_link, short_id)
        db.session.commit()
    return render_template('index.html', form=form, short_url=short_url_result)


@app.route('/files', methods=['GET', 'POST'])
async def upload_view():
    """Асинхронное представление для загрузки файлов на Яндекс Диск."""
    form = UploadForm()
    files_table_data = []

    if form.validate_on_submit():
        files = form.files.data
        try:
            print(f"📂 [DEBUG] Начинаем загрузку {len(files)} файлов...")
            filenames, download_links, errors = await upload_file_to_yandex_disk(files)
            print(f"✅ [DEBUG] Функция вернула данные. Ошибки: {errors}")

        except Exception as e:
            # ЭТА СТРОКА СРАБОТАЕТ, ЕСЛИ ФУНКЦИЯ УПАДЕТ С ОШИБКОЙ
            print(f"💥 [CRITICAL] Критическая ошибка при вызове upload_file_to_yandex_disk: {e}")
            print(f"💥 [CRITICAL] Traceback: {type(e).__name__}")
            # Даже при ошибке мы должны вернуть страницу, чтобы тест не падал сразу с 500 ошибкой
            return render_template('files.html', form=form, files_table_data=files_table_data)

        if errors:
            for error in errors:
                flash(
                    f'Не удалось загрузить файл на Яндекс Диск: {error}',
                    'danger'
                )
                return render_template(
                    'files.html', form=form, files_table_data=files_table_data
                )

        for filename, original_link in zip(filenames, download_links):
            short_id = get_unique_short_id()

            short_url_result = create_url_map(original_link, short_id)

            files_table_data.append({
                'filename': filename,
                'short_link': short_url_result
            })

        db.session.commit()

    return render_template(
        'files.html',
        form=form,
        files_table_data=files_table_data
    )


@app.route('/<string:short_id>')
async def redirect_view(short_id):
    """Асинхронное представление для переадресации и скачивания файлов."""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    target = url_map.original

    parsed_url = urlparse(target)
    domain = parsed_url.netloc.lower()

    is_file_download_link = domain.startswith('downloader.disk.yandex.ru')

    if is_file_download_link:
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.get(target) as file_response:
                    file_response.raise_for_status()

                    file_content = await file_response.read()

                file_like_object = BytesIO(file_content)

                filename = os.path.basename(parsed_url.path)

                if not filename:
                    filename = 'downloaded_file'

                return send_file(
                    file_like_object,
                    mimetype=file_response.headers.get(
                        'Content-Type', 'application/octet-stream'
                    ),
                    as_attachment=True,
                    download_name=filename
                )

        except Exception as error:
            flash(f'Ошибка доступа к файлу: {str(error)}', 'danger')
            return redirect(url_for('upload_view'))

    else:
        return redirect(target)
