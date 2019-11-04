from app import app
from flask import render_template, request, jsonify, abort, make_response
from sql_f import SQLITE
from zabbix import ZABBIX
from Manager import *

def error_decorator(error_message):

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as ex:

                return jsonify( { 'result': False } ), 400

        return wrapper

    return decorator


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@app.route('/')
def index():
    sql = SQLITE()
    data = sql.get_tasks()
    return render_template('main_page.html', data_table = data)

@app.route('/delete_task/<int:item_id>', methods=['POST'])
def delete_task(item_id):
    print(item_id)
    sql = SQLITE()
    sql.delete_task(item_id)
    return index()

@app.route('/items/<int:task_id>/<int:group_id>/<int:host_id>/<group>/<id>')
def task_items_table(task_id, group_id, host_id, group, id):
    sql = SQLITE()
    data = sql.get_items_from_id(host_id)
    return render_template('item_table.html',  task=task_id, group_id = group_id,
                           data_table = data, name = id,
                           host = host_id, group=group)


@app.route('/task_create')
def task_create():
    return render_template('task.html')

@app.route('/send/<int:task_id>', methods = ['POST'])
def send(task_id):
    task(task_id)
    return index()

@app.route('/cron/<int:task_id>', methods = ['POST'])
def cron(task_id):
    sql = SQLITE()
    data = sql.get_cron_data(task_id)
    return render_template('cron.html',   data_table = data, task = task_id)

@app.route('/cron_add/<int:task_id>')
def cro_addn(task_id):

    return render_template('cron_create.html', task = task_id)


@app.route('/delete_cron/<int:id>/<int:task_id>', methods = ['POST'])
def delete_cron(id, task_id):
    sql = SQLITE()
    sql.delete_cron(id)
    return cron(task_id)



@app.route('/cron_add/<int:task_id>', methods = ['POST'])
def cro_add_post(task_id):
    fields = {
        'type': request.form['type'],
        'time': request.form['time'],
        'day': request.form['day']
    }
    if (fields['type'] == '0'):
        day = fields['day']
    else:
        day = -1
    sql = SQLITE()
    sql.add_new_cron_data(day, task_id, fields['time'])


    return cron(task_id)




@app.route('/task_create', methods = ['POST'])
def task_create_post():
    fields = {
        'task': request.form['task'],
        'title': request.form['title'],
        'begin': request.form['begin'],
        'end': request.form['end']

    }
    sql = SQLITE()
    sql.add_new_task(fields['task'], fields['title'], fields['begin'], fields['end'])
    return index()



@app.route('/emails/<int:task_id>', methods = ['POST'])
def mail_table(task_id):
    sql = SQLITE()
    data = sql.get_mail_to(task_id)

    return render_template('mail_to.html',   data_table = data, task = task_id)


@app.route('/mail_add/<int:task_id>')
def mail_add(task_id):

    return render_template("mail_create.html")


@app.route('/groups/<int:item_id>')
def groups_table(item_id):
    sql = SQLITE()
    data = sql.get_groups(item_id)
    return render_template('groups_table.html',   data_table = data, data=item_id)

@app.route('/hosts/<int:task_id>/<int:group_id>/<id>')
def hosts_table(task_id,  group_id, id):
    print (id)
    sql = SQLITE()
    data = sql.get_hosts(group_id)
    return render_template('hosts_table.html',   data_table = data,
                           task=task_id, group = group_id, name = id)


@app.route('/delete_host/<int:task_id>/<int:group_id>/<id>/<int:host_id>',
           methods=['POST'])
def delete_host(task_id, group_id, id, host_id):
    print (id)
    sql = SQLITE()
    sql.delete_host(host_id)
    return hosts_table(task_id, group_id, id)


@app.route('/hosts_add/<int:task_id>/<int:group_id>/<id>')
def add_hosts(task_id, group_id, id):
    sql = SQLITE()

    zab =get_zabbix()
    hosts = zab.get_host(sql.get_group_zabbix_id(group_id))
    tmp = []
    for object in hosts:
        tmp.append(object['host'])
    return render_template("hosts_create.html", data_table = tmp)



@app.route('/groups_add/<int:item_id>')
def list_group_add(item_id):
    zab = get_zabbix()
    data = zab.get_groups()
    tmp = []
    for i in data:
        tmp.append(i['name'])
    return render_template("groups_create.html", data_table = tmp)



@error_decorator('error add group')
@app.route('/mail_add/<int:task_id>', methods = ['POST'])
def add_new_email(task_id):
    fields = {
        'email': request.form['email'],
        'comment': request.form['comment'],

    }
    sql = SQLITE()
    sql.add_new_mail_to(fields['email'], fields['comment'], task_id)
    return mail_table(task_id)

@app.route('/delete_mail/<int:item_id>/<int:task_id>', methods=['POST'])
def delete_mails(item_id, task_id):
    sql = SQLITE()
    sql.delete_email(item_id)
    return mail_table(task_id)

@error_decorator('error add group')
@app.route('/groups_add/<int:item_id>', methods = ['POST'])
def add_new_group(item_id):
    fields = {
        'group': request.form['group'],
        'comment': request.form['comment'],

    }
    zab = get_zabbix()
    data = zab.get_groups()
    zab_id = None
    for i in data:
        if i['name'] == fields['group']:
            zab_id = i['groupid']
    sql = SQLITE()
    sql.add_new_group(fields['group'], fields['comment'], item_id, zab_id)
    return groups_table(item_id)

@app.route('/delete_groups/<int:task_id>/<int:item_id>', methods=['POST'])
def delete_group(task_id, item_id):
    sql = SQLITE()
    sql.delete_group(item_id)
    return groups_table(task_id)


@app.route('/item_create/<int:task_id>/<int:group_id>/<id>/<int:host_id>/<id_h>/')
def item_create(task_id, group_id, host_id, id, id_h):
    zab = get_zabbix()
    sql = SQLITE()
    rez = sql.get_host_zabbix_id(host_id)
    items = zab.get_item(rez)
    return render_template("task_create.html", data_table = items, task = task_id,
                           group = group_id, host = host_id)


@app.route('/delete_item/<int:item_id>/<int:task_id>/<int:group_id>/<group>/<int:host_id>/<id>', methods=['POST'])
def delete_item(item_id, task_id, group_id, group, host_id, id):
    print(item_id)
    sql = SQLITE()
    sql.delete_item_data(item_id)
    return task_items_table(task_id, group_id, host_id, group, id)

@app.route('/hosts_add/<int:task_id>/<int:group_id>/<id>', methods = ['POST'])
def task_host_create(task_id, group_id, id):
    fields = {
        'host': request.form['host'],
        'comment': request.form['comment'],

    }
    sql = SQLITE()
    zab = get_zabbix()
    hosts = zab.get_host(sql.get_group_zabbix_id(group_id))
    zab_id = None
    for i in hosts:
        if i['host'] == fields['host']:
            zab_id = i['hostid']

    sql.add_new_item_host(fields['host'], fields['comment'], task_id, group_id, zab_id)
    return hosts_table(task_id, group_id, id)


@error_decorator('error add item')
@app.route('/item_create/<int:task_id>/<int:group_id>/<id>/<int:host_id>/<id_h>/', methods = ['POST'])
def task_item_create(task_id, group_id, host_id, id, id_h):
    fields = {
        'item': request.form['item'],
        'comment': request.form['comment'],
        'new_name': request.form['new_name'],

    }
    sql = SQLITE()
    sql.add_new_item_data(fields['item'], fields['comment'], fields['new_name'],
                          task_id, host_id)
    return task_items_table(task_id, group_id, host_id, id, id_h)


def get_zabbix():
    zabbix = ZABBIX()
    zabbix.auth("Alexander", 'Nik9640707')
    return zabbix

#zab = get_zabbix()