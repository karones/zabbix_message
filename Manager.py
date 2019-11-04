from sql_f import SQLITE
import os
import ast
from zabbix import ZABBIX


def task (id):
    sql = SQLITE()

    Debug = True
    if True:
        html ="""
        <!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Отчет Zabbix</title>
</head>
<body>
<table border="1">
<caption>Отчет</caption>
<tr>
<th></th>
<th>Item</th>
<th>Значение</th>
<th>Комментарий</th>

</tr>"""
        zabbix = ZABBIX()
        zabbix.auth("login", 'password')
        task_list = sql.get_all_data_to_manager(id)
        last_group = ""
        last_host = ""
        print (task_list)

        list = []
        for data in task_list:
            list.append(ast.literal_eval(data[0])['itemid'])


        data_z = zabbix.get_items(list)
        result = {}
        for i in data_z:
            temp = i['itemid']
            result[str(temp)] = i


        check =  lambda T:  T[2] if T[2] != "" else T[0]
        for data in task_list:
            if last_group != data[5]:
                last_group = data[5]
                html += "<tr> <th>" + data[5] + "</th></tr>"
                #continue
            if last_host != data[3]:
                last_host = data[3]
                html += "<tr> <th></th><th></th><th></th><th></th></tr>"
                html += "<tr> <th></th><th>" + data[3] + "</th><th></th><th></th></tr>"
                #continue
            #if
            html += "<tr> <th></th><th>" + check(data)  + "</th><th>" \
                    + result[ast.literal_eval(data[0])['itemid']]['lastvalue']+"</th><th>" +\
                    data[1] + "</th></tr>"


        html += """</table>
    </body>
    </html>"""

        f = open('text.html', 'w')
        f.write(html)
        f.close()

        task = sql.get_task_data(id)

        mails = sql.get_mail_to_manager(id)

        mail = " ".join(mails)
        cmd = 'echo "' + task[0][3] + '\n\n\n' + task[0][4] + '" | mailx -v -r "' \
              + task[0][2] +'" -s "Tor notification" ' \
     '-S smtp="192.168.10.10:25" -a "./text.html" ' + mail
     #    cmd = 'cat text.html | mailx -v -r "Monitoing@tor-service.ru" ' \
     #          '-s "$(echo "This is the subject\nContent-Type: text/html")" ' \
     #          '-S smtp="192.168.10.10:25" -a "./text.html" ' + mail
        print (cmd)
        os.system(cmd)#


if __name__ == '__main__':

    task(1)
