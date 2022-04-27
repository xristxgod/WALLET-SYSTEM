from flask_apscheduler import APScheduler

def register_scheduler(app):
    scheduler = APScheduler()
    scheduler.init_app(app)

    # scheduler.add_job(id='Func info', func=func_name, trigger='cron', hour=23, minute=00)

    scheduler.start()