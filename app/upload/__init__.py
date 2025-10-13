from flask import Blueprint
from flask_restful import Api

upload_blueprint = Blueprint("upload", __name__)
api = Api(upload_blueprint)

from .upload import FileDownload, FileUpload

api.add_resource(FileUpload, "/api/upload-file", endpoint="file_upload")
api.add_resource(
    FileDownload, "/api/uploads/<string:filename>", endpoint="file_download"
)
