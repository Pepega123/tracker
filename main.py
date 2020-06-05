import datetime
import hashlib
import logging
import os
import psutil 
import psycopg2
import time
import atexit
from db import *

logger = logging.getLogger('tracker')
logger.setLevel(logging.DEBUG)

TOTAL_MINUTES = 0
NEW_DAY = False
START_TIME = 0
CURRENT_DATE = datetime.date.today()
CONN = psycopg2.connect(**config())
CUR = CONN.cursor()


def get_hash(filename):
   # make a hash object
   h = hashlib.sha1()
   # open file for reading in binary mode
   with open(filename,'rb') as file:
       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)
   # return the hex representation of digest
   return h.hexdigest()

def find_proc_by_hash(hash="fdd2fe36c6e859779f8e5e65155acf55d625f7f1"):
    #find by hash
    for p in psutil.process_iter():
        try:
            #reduce computational intensity, remove for more thorough search
            if("C:\\Program Files (x86)\\" in p.exe()):
                if get_hash(p.exe()) == hash:
                    return True
        except (psutil.AccessDenied, FileNotFoundError): 
            pass
    return False
    
def calc_time_diff(start_time, end_time):
    return int(time.mktime(end_time.timetuple()) - time.mktime(start_time.timetuple())) / 60
    
def execute_stmt(date, minutes, cur):
    global NEW_DAY
    #print(NEW_DAY)
    #new day, create new entry:
    if(NEW_DAY): 
        stmnt = "INSERT INTO times(date, minutes) VALUES (\'" + str(date) + "\', " + str(minutes) + ");"
        NEW_DAY = False
    #same day, update entry:
    else:  
         stmnt = "UPDATE times SET minutes = " + str(minutes) + " WHERE date = \'" + str(date) + "\';"
    logger.debug(stmnt)
    cur.execute(stmnt)

def init():
    fh = logging.FileHandler('log/spam.log')
    fh.setLevel(logging.DEBUG)
    
    info = logging.FileHandler('log/info.log')
    info.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    fh.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(info)
    
    logger.debug("-------------------------------")
    logger.debug("STARTING APPLICATION")
    

def main():
    logger.info("Initializing tracker")
    init()
    stmnt = ""
    global TOTAL_MINUTES
    global NEW_DAY
    global START_TIME
    global CURRENT_DATE
    UPDATE_INTERVAL = 10
    INITIAL_INTERVAL = 10
    CURRENT_DATE = datetime.date.today()
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    
    #proc_closed = True
    #queried_after_close = False
    
    #print(get_hash("C:\\Program Files (x86)\\World of Warcraft\\_classic_\\abc.exe"))
    
    # get date from previous run
    stmnt = "SELECT date FROM last_run;"
    cur.execute(stmnt)
    last_run_date = cur.fetchall()[0][0]
    logger.debug(stmnt)
    logger.debug(str(last_run_date))
    
    if str(last_run_date) != str(CURRENT_DATE):
        NEW_DAY = True
    #same day, start counting from already counted hours 
    else:
        stmnt = "SELECT minutes FROM times WHERE date = \'" + str(CURRENT_DATE) + "\';"
        cur.execute("SELECT minutes FROM times WHERE date = \'" + str(CURRENT_DATE) + "\';")
        TOTAL_MINUTES += cur.fetchall()[0][0]
        logger.debug(stmnt)
        logger.debug(str(TOTAL_MINUTES))
    
    #TODO: maybe close connection to DB here and reopen at end?
    
    #outer while, wait for application to be opened
    while(True):
        
        time.sleep(INITIAL_INTERVAL)
        process_running = "WowClassic.exe" in (p.name() for p in psutil.process_iter()) or find_proc_by_hash()


        #process found 
        if(process_running): 
            logger.info("Process started!")
            START_TIME = datetime.datetime.now()
           #inner while, count time app is open
            while("WowClassic.exe" in (p.name() for p in psutil.process_iter()) or find_proc_by_hash()):
               logger.info("WoW running still...") #TODO: ADD LOGGING STATEMENTS
               time.sleep(UPDATE_INTERVAL) #wait 10 seconds between checks
            end_time = datetime.datetime.now()
            
            #calculate amount of time application was open 
            elapsed_minutes = calc_time_diff(START_TIME, end_time)
            TOTAL_MINUTES = TOTAL_MINUTES + elapsed_minutes
        #wait for process to start
        else:
            continue

        logger.info("Total time active this session: " + str(elapsed_minutes))
        logger.info("Total time active today: " + str(TOTAL_MINUTES))
        
        #update last_run
        cur.execute("UPDATE last_run SET date = \'" + str(CURRENT_DATE) + "\';")
        
        #update/insert into times
        execute_stmt(CURRENT_DATE, TOTAL_MINUTES, cur)
        
        #update times
        #new day, create new entry:
        # if(NEW_DAY):
            # stmnt = "INSERT INTO times(date, minutes) VALUES (\'" + str(CURRENT_DATE) + "\', " + str(TOTAL_MINUTES) + ");"
            # logger.debug(stmnt)
            # cur.execute(stmnt)
            # #process has been closed, if it is opened again later it is (most likely) on the same day
            # NEW_DAY = False
        # #same day, update entry:
        # else:
            # stmnt = "UPDATE times SET minutes = " + str(TOTAL_MINUTES) + " WHERE date = \'" + str(CURRENT_DATE) + "\';"
            # logger.debug(stmnt)
            # cur.execute("UPDATE times SET minutes = " + str(TOTAL_MINUTES) + " WHERE date = \'" + str(CURRENT_DATE) + "\';")
            # cur.execute(stmnt)
            

        
        conn.commit()
        #start counting fresh next time process is opened
        #TOTAL_MINUTES = 0
        
        
    #never reached, maybe close/open before each update instead?
    #conn.close()

#cleanup, log times before exiting 
atexit.register(execute_stmt, CURRENT_DATE, TOTAL_MINUTES, CUR)


if __name__ == "__main__":
    main()