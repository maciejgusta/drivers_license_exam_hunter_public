from apscheduler.schedulers.blocking import BlockingScheduler
from scraper import run_scraper
from sender import run_sender
from datetime import datetime

# SPECIFY THE EXAMINATION CENTER, CATEGORY, EXAM TYPE AND TIME INTERVAL
PROVINCE = "mazowieckie"
ORGANIZATION = "bemowo"
CATEGORY = "B"
HEADLESS = True
TIMEDELTA_DAYS = 14
EXAM_TYPE = True # SPECIFY EXAM TYPE: True - practical, False - theoretical

last_exam = None

def job():
    global last_exam
    print(f"\n{datetime.now().strftime('%H:%M:%S')} Running scraper...")
    result = run_scraper(PROVINCE, ORGANIZATION, CATEGORY, HEADLESS, EXAM_TYPE)
    if result['error'] is None:
        exam_date = result['exam_datetime']

        print(f"Scrape successfull: Found exam date: {exam_date.strftime('%d.%m.%Y %H:%M')}")


        if last_exam is None or last_exam != exam_date:
            sending_status = run_sender(PROVINCE=PROVINCE, ORGANIZATION=ORGANIZATION, CATEGORY=CATEGORY, DATETIME=exam_date, TIMEDELTA_DAYS=TIMEDELTA_DAYS, EXAM_TYPE=EXAM_TYPE)
            if (sending_status):
                print('Email sent!')
            else:
                print('Email not sent')

        last_exam = exam_date

    else:
        print('Error when scraping')

scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', seconds=20, next_run_time=datetime.now())

try:
    print("Scheduler started. Press Ctrl+C to exit.")
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Scheduler stopped.")