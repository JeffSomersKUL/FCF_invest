from flask import jsonify
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import BaseView, expose


class BaseAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class LogView(BaseView):
    def __init__(self, log_file, title, *args, **kwargs):
        super(LogView, self).__init__(*args, **kwargs)
        self.log_file = log_file
        self.title = title

    @expose("/")
    def index(self):
        return self.render("admin/log_view.html", title=self.title)

    @expose("/logs", methods=["GET"])
    def get_logs(self):
        try:
            with open(self.log_file, "r") as f:
                content = f.readlines()
        except Exception as e:
            return jsonify({"error": f"Could not read log file: {e}"}), 500

        # Return the log content as JSON
        return jsonify({"logs": content})
