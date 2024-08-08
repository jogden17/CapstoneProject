from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import subprocess

# Define the job function
def job():
    print(f"Task is running at {datetime.datetime.now()}")
    # Run your script
    subprocess.run(["python3", "./main.py"])
    print(f"Task is done at {datetime.datetime.now()}")

# Create an instance of the scheduler
scheduler = BlockingScheduler()

# Schedule the job to run every 24 hours
scheduler.add_job(job, 'interval', hours=24)

try:
    # Start the scheduler
    print("Starting scheduler...")
    scheduler.start(job())
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler if interrupted
    print("Shutting down scheduler...")
    scheduler.shutdown()
