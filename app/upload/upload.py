import os
from flask import (
    request,
    jsonify,
    send_from_directory,
    url_for,
    current_app,
)
from werkzeug.utils import secure_filename
from flask_ckeditor import upload_fail
import magic
from flask_restful import Resource

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg"}


def allowed_file_type(file):
    mime = magic.Magic(mime=True)
    file_mime_type = mime.from_buffer(file.read(2048))
    file.seek(0)
    return file_mime_type in ALLOWED_MIME_TYPES


class FileUpload(Resource):
    def post(self):
        if "upload" not in request.files:
            return upload_fail(message="No file uploaded")

        f = request.files.get("upload")

        if f.filename == "":
            return upload_fail(message="No selected file")

        if not allowed_file_type(f):
            return upload_fail(message="Invalid file type, only images")

        filename = secure_filename(f.filename)
        upload_path = current_app.config["UPLOAD_PATH_IMAGES"]
        filepath = os.path.join(upload_path, filename)
        f.save(filepath)

        file_url = url_for(
            "upload.file_download", filename=filename, _external=True
        )
        return jsonify({"uploaded": 1, "fileName": filename, "url": file_url})


class FileDownload(Resource):
    def get(self, filename):
        return send_from_directory(
            current_app.config["UPLOAD_PATH_IMAGES"], filename
        )
