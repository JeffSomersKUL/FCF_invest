import logging
from .base_view import BaseAdmin
from flask_admin import BaseView, expose
from app.scheduler import get_job_id


class ScheduledTaskAdmin(BaseAdmin):
    form_columns = ["name", "run_time", "active", "type", "period"]
    category = "Scheduler"

    def after_model_change(self, form, model, is_created):
        from app.scheduler import schedule_task

        schedule_task(model)

    def after_model_delete(self, model):
        from app.scheduler import scheduler

        job_id = get_job_id(model)
        if scheduler.get_job(job_id):
            scheduler.remove_job(job_id)
            logging.info(f"Removed job for deleted task ID {model.id}")


class SchedulerJobsView(BaseView):
    @expose("/")
    def index(self):
        from app.scheduler import scheduler

        jobs = scheduler.get_jobs()
        return self.render("admin/jobs_view.html", jobs=jobs)
