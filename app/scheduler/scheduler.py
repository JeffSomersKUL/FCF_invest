from flask import current_app
from .models import ScheduledTask, TaskType, Period
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler

from app import scheduler_logger, db

scheduler = APScheduler()


def init_scheduler(app):
    scheduler.init_app(app)
    scheduler.start()
    schedule_tasks()


def get_job_id(task):
    return task.uid


def schedule_tasks():
    with scheduler.app.app_context():
        tasks = []
        try:
            tasks = ScheduledTask.query.filter_by(active=True).all()
        except Exception:
            scheduler_logger.warning("Could not find current tasks")
        for task in tasks:
            try:
                schedule_task(task)
            except Exception:
                scheduler_logger.warning(f"Could not initialize {task}")


def schedule_task(task):
    job_id = get_job_id(task)
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    if task.active:
        task_func = get_task_function(task.type)
        if not task_func:
            scheduler_logger.warning(
                f"Unknown task type {task.type} for task ID {task.id}"
            )
            return

        if task.period == Period.DAILY:
            schedule_daily_job(task, task_func, job_id)
        elif task.period == Period.ONCE:
            schedule_once_job(task, task_func, job_id)


def get_task_function(task_type):
    if task_type == TaskType.SAVE_STOCK_PRICE:
        return save_stock_price
    else:
        return None


def schedule_daily_job(task, task_func, job_id):
    job = scheduler.add_job(
        func=task_func,
        trigger="cron",
        id=job_id,
        name=task.type.value,
        hour=task.run_time.hour,
        minute=task.run_time.minute,
        second=task.run_time.second,
        replace_existing=True,
    )
    scheduler_logger.info(
        f"Scheduled daily job {task.name} (ID: {task.uid}) "
        f"to run at {job.next_run_time}"
    )


def schedule_once_job(task, task_func, job_id):
    now = datetime.now()
    run_datetime = datetime.combine(now.date(), task.run_time)
    if run_datetime < now:
        run_datetime += timedelta(days=1)
    scheduler.add_job(
        func=run_once_job,
        trigger="date",
        id=job_id,
        name=task.type.value,
        run_date=run_datetime,
        args=[task.id, task_func],
        replace_existing=True,
    )
    scheduler_logger.info(
        f"Scheduled one-time job {task.name} (ID: {task.uid}) "
        f"to run at {run_datetime}"
    )


def run_once_job(id, task_func):
    with scheduler.app.app_context():
        try:
            scheduler_logger.info(f"Executing one-time job ID: {id}")
            task = ScheduledTask.query.get(id)
            if not task:
                scheduler_logger.error(f"Task ID {id} not found.")
                return
            # Execute the associated function
            task_func()
            # Deactivate the task after running
            task.active = False
            db.session.commit()
            scheduler_logger.info("Corresponding task has been deactivated.")
        except Exception as e:
            scheduler_logger.error(
                f"Error executing one-time job ID {id}: {e}"
            )


def save_stock_price():
    """Dummy function to simulate saving stock price."""
    try:
        scheduler_logger.info(
            "Executing SaveStockPrice task: Saving stock price..."
        )
        # Your logic to save stock price goes here
        # ...
        scheduler_logger.info("Stock price saved successfully.")
    except Exception as e:
        scheduler_logger.error(f"Error executing SaveStockPrice task: {e}")
