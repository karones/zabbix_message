import datetime
import calendar
from Manager import *
from sql_f import SQLITE

class CRON:
    def check(self):
        sql = SQLITE()
        data = sql.get_cron_all_data()
        print(data)
        now = datetime.datetime.now()
        print (now.day)
        print (now.year)
        print (now.minute)
        for i in data:
            datetime_object = datetime.datetime.strptime(str(now.year) + ":" +
                                                         str(now.month) + ":" +
                                                         str(now.day) + " " +i[3],
                                                         "%Y:%m:%d %H:%M")
            print(datetime_object.strftime("%Y:%m:%d %H:%M"))
            print(now.strftime("%Y:%m:%d %H:%M"))

            if i[1] == '-1':
                day = calendar.monthrange(now.year, now.month)[1]
            else:
                day = i[1]


            if day == str(now.day):
                print((now - datetime_object).total_seconds())
                if 0 < (now - datetime_object).total_seconds() < 605:
                    print('run')
                    task(int(i[2]))





if __name__=="__main__":
    # app.run(host="192.168.10.30")
    cron = CRON()
    result = cron.check()