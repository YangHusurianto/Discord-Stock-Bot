import time
import sched
import neocities
import os
import shutil
from datetime import datetime, timedelta
from tokens import neocitiesToken as nc



nc = neocities.NeoCities('stonkman', nc) #Log into neocities account

wipeTime = '23:00' #Wipe time in 24h format

def wipeFiles(): #Wipe all local and neocities chart files
	for folder in os.listdir('./charts'): #Scans local directory to discover folders to delete
		nc.delete(folder)
		shutil.rmtree(f'./charts/{folder}')

def scheduleWipe():
	f = '%H:%M' #Time format
	timeNow = datetime.strftime(datetime.now(), f) #Current time in 24hr format
	timeUntil = (datetime.strptime(wipeTime, f) - datetime.strptime(timeNow, f)).total_seconds() #Time in seconds until wipeTime

	s = sched.scheduler(time.perf_counter, time.sleep) #Creates a scheduler
	s.enter(timeUntil, 1, wipeFiles) #Sets the scheduler to run wipeFiles at wipeTime 
	