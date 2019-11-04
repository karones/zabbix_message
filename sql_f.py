
import sqlite3


class SQLITE:
    def __init__(self):
        self.__conn = sqlite3.connect("./mydatabase.db")
        self.__cursor = self.__conn.cursor()

    def get_group_zabbix_id(self, id):
        sql = "SELECT * FROM groups WHERE id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data[0])

    def get_host_zabbix_id(self, id):
        sql = "SELECT * FROM hosts WHERE id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data[0])



    def add_new_group(self, group, comment, task_id, zab_id):
        sql = "INSERT INTO 'groups' (text, comment, task_id, zabbix_id)" \
              " VALUES (?, ?, ?, ?)"
        self.__cursor.execute(sql, [(group), (comment), (task_id), zab_id])
        self.__conn.commit()


    def add_new_mail_to(self, mail, comment, task_id):
        sql = "INSERT INTO mail_to (mail, comment, task_id) VALUES (?, ?, ?)"
        self.__cursor.execute(sql, [(mail), (comment), task_id])
        self.__conn.commit()


    def get_mail_to(self, id):
        sql = "SELECT * FROM mail_to WHERE task_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)

    def add_new_cron_data(self,  str, id, time):
        sql = "insert into cron ( data, task_id, time) " \
              "VALUES (?, ?, ?)"
        self.__cursor.execute(sql, [(str), (id), time])
        self.__conn.commit()

    def add_new_item_host(self, text, comment, task_id, group_id, zabbix_id):
        sql = "insert into hosts (name, comment, task_id, group_id, zabbix_id) " \
              "VALUES (?, ?, ?, ?, ?)"
        self.__cursor.execute(sql, [text, comment, task_id, group_id, zabbix_id])
        self.__conn.commit()


    def add_new_item_data(self, text, comment, new_name, task_id, host_id):
        sql = "insert into items ( name, comment, user_text, task_id, host_id) " \
                  "VALUES ( ?, ?, ?, ?, ?)"
        self.__cursor.execute(sql, [text, comment, new_name, task_id, host_id])
        self.__conn.commit()

    def delete_group(self, id):
        sql = "DELETE FROM 'groups' WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()

    def delete_email(self, id):
        sql = "DELETE FROM mail_to WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()


    def delete_item_data(self, id):
        sql = "DELETE FROM items WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()

    def get_items_from_id(self, id ):
        sql = "SELECT * FROM items WHERE host_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)


    def get_items(self, id, groups):
        sql = "SELECT * FROM items WHERE task_id = ? and "
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return (data)

    def get_groups(self, id):
        sql = "SELECT * FROM 'groups' WHERE task_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)

    def get_group_from_id (self, id):
        sql = "SELECT name FROM 'groups' WHERE task_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data[0])

    def get_hosts(self, id):
        sql = "SELECT * FROM 'hosts' WHERE group_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)

    def get_tasks(self):
        sql = "SELECT * FROM tasks"
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return (data)

    def delete_task(self, id):
        sql = "DELETE FROM tasks WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()

    def delete_cron(self, id):
        sql = "DELETE FROM cron WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()



    def delete_host(self, id):
        sql = "DELETE FROM hosts WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()

    def get_data_mail(self):
        sql = "SELECT server, login, password,  from_mail FROM mail WHERE id = 1"
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return (data[0])

    def get_cron_all_data(self):
        sql = "SELECT * FROM cron "
        self.__cursor.execute(sql, )
        data = self.__cursor.fetchall()
        return (data)



    def get_cron_data(self, id):
        sql = "SELECT * FROM cron WHERE task_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)

    def get_items(self):
        sql = "SELECT * FROM items"
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return (data)

    def get_hosts_from_group(self, task, group):
        sql = "SELECT * FROM hosts WHERE task_id = ? and group_id = ?"
        self.__cursor.execute(sql, [task, group])
        data = self.__cursor.fetchall()
        return (data)



    def get_groups_list(self):
        sql = "SELECT text FROM 'groups'"
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        return (data)


    def get_all_data_to_manager(self, task_id):
        sql = """SELECT items.name, items.comment, items.user_text, hosts.name, hosts.zabbix_id, groups.text, 
        groups.zabbix_id FROM items, groups,
                                   hosts WHERE items.task_id = ? and
                        items.host_id = hosts.id and hosts.group_id = groups.id 
                        order by groups.text, hosts.name"""
        self.__cursor.execute(sql, [task_id])
        data = self.__cursor.fetchall()
        return (data)


    def get_task_data(self, id):
        sql = "SELECT * FROM tasks where id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        return (data)

    def add_new_task(self, text, title, begin, end):
        sql = "insert into tasks (name, title, text_begin, text_end) " \
              "VALUES (?, ?, ?, ?)"
        self.__cursor.execute(sql, [text, title, begin, end])
        self.__conn.commit()

    def delete_task(self, id):
        sql = "DELETE FROM tasks WHERE id = ?"
        self.__cursor.execute(sql, [id])
        self.__conn.commit()

    def get_mail_to_manager(self, id):
        sql = "SELECT mail FROM mail_to WHERE task_id = ?"
        self.__cursor.execute(sql, [id])
        data = self.__cursor.fetchall()
        list = []
        for i in data:
            list.append(i[0])
        return (list)