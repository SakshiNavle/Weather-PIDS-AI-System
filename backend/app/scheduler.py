
from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks import weather_prediction_job


scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(
        weather_prediction_job,

        trigger="interval",

        minutes=5,

        id="weather_prediction_job",

        replace_existing=True,
    )

    scheduler.start()

    print("Scheduler Started")

