from apscheduler.schedulers.blocking import BlockingScheduler
import dataScrape

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=30)
def timed_job():
    #print('This job is run every three minutes.')
    dataScrape.getData()

sched.start()