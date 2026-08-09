from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks import update_weather


scheduler = BackgroundScheduler()


def start_scheduler():

    # Avoid duplicate jobs if scheduler is initialized again
    if scheduler.get_job("weather_update_job"):
        return

    scheduler.add_job(
        update_weather,
        trigger="interval",
        minutes=5,
        id="weather_update_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print("Scheduler Started")


def stop_scheduler():

    if scheduler.running:
        scheduler.shutdown(wait=False)
        print("Scheduler Stopped")