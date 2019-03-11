import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import argparse
import os

# To run the script when booting
# sudo cp -i /path/to/your_script.py /bin
# sudo crontab -e
# Add this line: @reboot python3 daily_backup.py -i Path/To/Database -b Path/To/Backup -t 2 &

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--InputPath', help='Path of the data to backup.', type=str, action = 'store', required = True)
parser.add_argument('-b', '--BackupPath', help='Patch to the backup folder.', type=str, action = 'store', required = True)
parser.add_argument('-t', '--BackupTime', help='Hour of the daily backup.', type=int, action = 'store', required = True)

args = parser.parse_args()

input_path = args.InputPath
backup_path = args.BackupPath
backup_time = args.BackupTime

# First backup:
arguments = ['cp', '-rf', input_path, backup_path]
os.system(arguments)

sched = BlockingScheduler()
sched.start()

def ProcessBackup():
    with open(backup_path + '/BackupStat.txt', 'w') as out:
        arguments = ['cp', '-rf', input_path, backup_path]
        os.system(' '.(arguments))
        out.write('Backup done: ' + str(datetime.datetime.now()) + '\n')
        time.sleep(20)

sched.add_cron_job(ProcessBackup,  hour = backup_time)
