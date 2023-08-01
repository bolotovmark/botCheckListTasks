import sqlite3
from datetime import datetime

conn = sqlite3.connect('db.sqlite')


async def db_exists_user(user_id):
    try:

        cur = conn.cursor()
        rez = cur.execute(f"SELECT id_user, id_position_user, name, name_position FROM users "
                          f"JOIN positions p on p.id_position = users.id_position_user "
                          f"WHERE id_user = {user_id};")
        user = rez.fetchone()
        cur.close()
        return user
    except:
        return False


async def db_insert_new_user(user_id, position_id, name):
    cur = conn.cursor()
    data_insert = (user_id, position_id, name)
    cur.execute("INSERT INTO users(id_user, id_position_user, name) VALUES (?, ?, ?);", data_insert)
    conn.commit()
    cur.close()


async def db_remove_user(user_id: str):
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute(f"DELETE FROM users WHERE id_user = {user_id};")
    conn.commit()
    cur.close()


async def db_get_list_user():
    cur = conn.cursor()
    cur.execute("SELECT name, name_position, id_user FROM users "
                "JOIN positions p on p.id_position = users.id_position_user "
                "ORDER BY name ASC;")
    users = cur.fetchall()
    cur.close()
    return users


async def db_get_list_types_event_offset(offset):
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT id_type, name_type FROM daily_tasks "
                f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                f"JOIN type_event te on te.id_type = e.id_type_event "
                f"WHERE date_task = date('now','localtime', '{offset} day') "
                f"ORDER BY name_type;")
    types = cur.fetchall()
    cur.close()
    return types


async def db_get_list_types_event():
    cur = conn.cursor()
    cur.execute(f"SELECT DISTINCT id_type, name_type FROM event "
                f"JOIN type_event te on te.id_type = event.id_type_event "
                f"WHERE id_type != 1")
    types = cur.fetchall()
    cur.close()
    return types



async def db_insert_new_type_event(name_type):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO type_event(name_type) VALUES ('{name_type}');")
    conn.commit()
    cur.execute("SELECT last_insert_rowid();")
    type_id = cur.fetchone()
    cur.close()
    return type_id


async def db_insert_new_event(name_event, id_event):
    cur = conn.cursor()
    data_insert = (name_event, id_event)
    cur.execute("INSERT INTO event(name_event, id_type_event) VALUES (?, ?);", data_insert)
    conn.commit()
    cur.close()


async def db_insert_new_event_3(name_event, id_event, group_name):
    cur = conn.cursor()
    data_insert = (name_event, id_event, group_name)
    cur.execute("INSERT INTO event(name_event, id_type_event, group_text) VALUES (?, ?, ?)", data_insert)
    conn.commit()
    cur.close()


async def db_get_name_type_event(id_type_event):
    cur = conn.cursor()
    cur.execute(f"SELECT name_type FROM type_event WHERE id_type = {id_type_event};")
    name_type_event = cur.fetchone()
    cur.close()
    return name_type_event


async def db_get_list_events():
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT name_event, name_type FROM event "
                    f"Join type_event te on te.id_type = event.id_type_event "
                    f"ORDER BY id_type ASC")
        list_events = cur.fetchall()
        cur.close()
        return list_events
    except:
        return False


async def db_get_list_events_type(id_type):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM event "
                    f"JOIN type_event te on te.id_type = event.id_type_event "
                    f"WHERE id_type = {id_type} "
                    f"ORDER BY group_text ASC;")
        list_events_type = cur.fetchall()
        cur.close()
        return list_events_type
    except:
        return False


async def db_get_list_events_type_offset(id_type, offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM event "
                    f"JOIN type_event te on te.id_type = event.id_type_event "
                    f"WHERE id_type = {id_type} "
                    f"ORDER BY group_text ASC "
                    f"LIMIT {offset}, 5")
        list_events_type = cur.fetchall()
        cur.close()
        return list_events_type
    except:
        return False


async def db_remove_event(id_event):
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute(f"DELETE FROM event WHERE id_event = {id_event};")
        conn.commit()
        cur.close()
    except:
        return False


async def db_remove_type(id_type):
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute(f"DELETE FROM type_event WHERE id_type = {id_type}")
        conn.commit()
        cur.close()
    except:
        return False


async def db_get_list_schedule_type(id_type):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT name_event, group_text, name_type FROM list_schedule "
                    f"JOIN event e on e.id_event = list_schedule.id_event_schedule "
                    f"JOIN type_event te on e.id_type_event = te.id_type "
                    f"WHERE id_type = {id_type} "
                    f"ORDER BY group_text ASC;")
        list_schedule = cur.fetchall()
        cur.close()
        return list_schedule
    except:
        return False


async def db_get_list_schedule_type_offset(id_type, offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_schedule, name_event, group_text, name_type FROM list_schedule "
                    f"JOIN event e on e.id_event = list_schedule.id_event_schedule "
                    f"JOIN type_event te on e.id_type_event = te.id_type "
                    f"WHERE id_type = {id_type} "
                    f"ORDER BY group_text ASC "
                    f"LIMIT {offset}, 5")
        list_schedule = cur.fetchall()
        cur.close()
        return list_schedule
    except:
        return False


async def db_insert_new_schedule_task(id_event):
    try:
        cur = conn.cursor()
        cur.execute(f"INSERT INTO list_schedule(id_event_schedule) VALUES ({id_event})")
        conn.commit()
        cur.close()
    except:
        return False


async def db_remove_schedule_task(id_task):
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute(f"DELETE FROM list_schedule WHERE id_schedule == {id_task}")
        conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        return False


async def db_get_list_daily_task_offset(offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_task, date_task, name_event, name_type, group_text  FROM daily_tasks "
                    f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                    f"JOIN type_event te on te.id_type = e.id_type_event "
                    f"WHERE date_task = date('now','localtime', '{offset} day');")
        list_tasks = cur.fetchall()
        cur.close()
        return list_tasks
    except:
        return False


async def db_get_list_daily_task_type(type_id, offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_task, date_task, name_event, name_type, group_text, mark, description, name FROM daily_tasks "
                    f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                    f"JOIN type_event te on te.id_type = e.id_type_event "
                    f"LEFT JOIN users u on u.id_user = daily_tasks.id_employee_schedule "
                    f"WHERE id_type = {type_id} AND date_task = date('now','localtime', '{offset} day') "
                    f"ORDER BY mark;")
        list_tasks = cur.fetchall()
        cur.close()
        return list_tasks
    except Exception as e:
        print(e)
        return False


async def db_get_list_daily_task_type_mark_false(type_id, offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_task, date_task, name_event, name_type, group_text, mark  FROM daily_tasks "
                    f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                    f"JOIN type_event te on te.id_type = e.id_type_event "
                    f"WHERE id_type = {type_id} "
                    f"AND date_task = date('now','localtime', '{offset} day') "
                    f"AND mark == false "
                    f"ORDER BY name_event;")
        list_tasks = cur.fetchall()
        cur.close()
        return list_tasks
    except:
        return False


async def db_get_list_daily_task_mark_false(day, page):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_task, date_task, name_event, name_type, group_text, mark  FROM daily_tasks "
                    f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                    f"JOIN type_event te on te.id_type = e.id_type_event "
                    f"WHERE date_task = date('now','localtime', '{day} day') "
                    f"AND mark == false "
                    f"ORDER BY name_type, name_event "
                    f"LIMIT {page}, 5;")
        list_tasks = cur.fetchall()
        cur.close()
        return list_tasks
    except:
        return False


async def db_insert_many_daily_task(list_tasks):
    try:
        cur = conn.cursor()
        cur.executemany("INSERT INTO daily_tasks(id_event_task) VALUES (?);", list_tasks)
        conn.commit()
        cur.close()
    except:
        return False


async def db_get_schedule_tasks():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id_event_schedule FROM list_schedule;")
        list_tasks = cur.fetchall()
        cur.close()
        return list_tasks
    except:
        return False


async def db_get_date_offset(offset):
    cur = conn.cursor()
    cur.execute(f"SELECT date('now', 'localtime', '{offset} day');")
    date = cur.fetchone()
    cur.close()
    return date


async def db_get_month_offset(offset):
    cur = conn.cursor()
    cur.execute(f"SELECT date('now', 'localtime', '{offset} month');")
    month = cur.fetchone()
    cur.close()
    return month


async def db_get_daily_task(task_id):
    cur = conn.cursor()
    cur.execute(f"SELECT id_task, name_event, name_type, group_text FROM daily_tasks "
                f"JOIN event e on e.id_event = daily_tasks.id_event_task "
                f"JOIN type_event te on te.id_type = e.id_type_event "
                f"WHERE id_task == {task_id}")
    task = cur.fetchone()
    cur.close()
    return task


async def db_check_mark_daily_task_id(task_id):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_task FROM daily_tasks "
                    f"WHERE id_task = {task_id} AND mark = false")
        task = cur.fetchone()
        cur.close()
        return task
    except:
        return False


async def db_update_daily_task(task_id, employee_id, description):
    try:
        cur = conn.cursor()
        cur.execute(f"UPDATE daily_tasks SET mark = true, "
                    f"id_employee_schedule = ?, description = ? "
                    f"WHERE id_task = ?", (employee_id, description, task_id))
        conn.commit()
        cur.close()
    except:
        return False


async def db_get_user_statistics_month(offset):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT id_user, name, SUM(mark) AS count FROM daily_tasks "
                    f"JOIN users u on u.id_user = daily_tasks.id_employee_schedule "
                    f"WHERE date_task "
                    f"BETWEEN date('now', 'start of month', '{offset} month') "
                    f"AND date('now', 'start of month', '{offset+1} month', '-1 day') "
                    f"AND id_employee_schedule IS NOT NULL "
                    f"AND mark = true "
                    f"GROUP BY id_employee_schedule "
                    f"ORDER BY name;")
        statistics = cur.fetchall()
        cur.close()
        return statistics
    except Exception as e:
        print(e)
        return False


async def list_schedule_task():
    types_event = await db_get_list_types_event()
    if types_event:
        name_type = types_event[0][1]
        out_text = f'*🔹{name_type}*\n'
        for type_event in types_event:
            if name_type != type_event[1]:
                name_type = type_event[1]
                out_text = out_text + f'\n\n*🔹{name_type}*\n'

            schedule_tasks = await db_get_list_schedule_type(type_event[0])

            if schedule_tasks:
                name_group = schedule_tasks[0][1]
                if name_group is None:
                    out_text = out_text + "  🔘*|Без группы|*\n"
                else:
                    out_text = out_text + f"  🔘*|{name_group}|*\n"
                i = 0
                for task in schedule_tasks:
                    i = i + 1
                    if name_group != task[1]:
                        i = 1
                        name_group = task[1]
                        out_text = out_text + f"\n  🔘*|{name_group}|*\n"
                    out_text = out_text + f"{i}. *{task[0]}*\n"

            else:
                out_text = out_text + '-'
    else:
        out_text = 'Список ежедневных задач пуст'

    return out_text


async def list_daily_task(offset):
    types_event = await db_get_list_types_event_offset(offset)
    date = await db_get_date_offset(offset)
    out_text = f"📆ДАТА: {date[0]}"
    if types_event:
        name_type = types_event[0][1]
        out_text = out_text + f'\n\n*🔹{name_type}*\n'
        for type_event in types_event:
            if name_type != type_event[1]:
                name_type = type_event[1]
                out_text = out_text + f'\n\n*🔹{name_type}*\n'

            schedule_tasks = await db_get_list_daily_task_type(type_event[0], offset)

            if schedule_tasks:
                name_group = schedule_tasks[0][4]
                if name_group is None:
                    out_text = out_text + "  🔘*|Без группы|*\n"
                else:
                    out_text = out_text + f"  🔘*|{name_group}|*\n"
                i = 0
                for task in schedule_tasks:
                    i = i + 1
                    if name_group != task[4]:
                        i = 1
                        name_group = task[4]
                        out_text = out_text + f"\n  🔘*|{name_group}|*\n"
                    # out_text = out_text + f"{i}. "
                    if bool(task[5]):
                        out_text = out_text + (f"\n{i}. ✅ *{task[2]}*\n"
                                               f"    👤Исполнитель: *{task[7]}*\n")
                        if not task[6] is None:
                            out_text = out_text + f"    📜Комментарий: *{task[6]}*\n"
                    else:
                        out_text = out_text + f"{i}. ❌ *{task[2]}*\n"

            else:
                out_text = out_text + '-'
    else:
        out_text = out_text + '\n\nСписок задач пуст'

    return out_text


async def list_daily_task_mark_false(offset):
    date = await db_get_date_offset(offset)
    out_text = f"📆ДАТА: {date[0]}"
    types_event = await db_get_list_types_event_offset(offset)
    if types_event:
        name_type = types_event[0][1]
        out_text = out_text + f'\n\n*🔹{name_type}*\n'
        for type_event in types_event:
            if name_type != type_event[1]:
                name_type = type_event[1]
                out_text = out_text + f'\n\n*🔹{name_type}*\n'

            schedule_tasks = await db_get_list_daily_task_type_mark_false(type_event[0], offset)

            if schedule_tasks:
                name_group = schedule_tasks[0][4]
                if name_group is None:
                    out_text = out_text + "  🔘*|Без группы|*\n"
                else:
                    out_text = out_text + f"  🔘*|{name_group}|*\n"
                i = 0
                for task in schedule_tasks:
                    i = i + 1
                    if name_group != task[4]:
                        i = 1
                        name_group = task[4]
                        out_text = out_text + f"\n  🔘*|{name_group}|*\n"
                    out_text = out_text + f"{i}. ❌ *{task[2]}*\n"
            else:
                out_text = out_text + '-'
    else:
        out_text = out_text + '\n\nСписок задач пуст'

    return out_text


async def list_month_statistics(offset):
    statistics = await db_get_user_statistics_month(offset)
    date = await db_get_month_offset(offset)

    date_object = datetime.strptime(date[0], '%Y-%m-%d').date()
    out_text = f"📆Период: *{date_object.strftime('%B %Y')}*\n"
    if statistics:
        for user in statistics:
            out_text += (f"\n\n"
                         f"👤 *{user[1]}*\n"
                         f"✅ Выполнено заданий: *{user[2]}*")

    else:
        out_text = out_text + '\n\nИнформация отсутствует'

    return out_text