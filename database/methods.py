import sqlite3

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


async def db_get_list_types_event():
    cur = conn.cursor()
    cur.execute("SELECT * FROM type_event;")
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
        cur.execute(f"SELECT name_event, group_text, name_type, name FROM list_schedule "
                    f"JOIN event e on e.id_event = list_schedule.id_event_schedule "
                    f"JOIN users u on u.id_user = list_schedule.id_author "
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
        cur.execute(f"SELECT id_schedule, name_event, group_text, name_type, name FROM list_schedule "
                    f"JOIN event e on e.id_event = list_schedule.id_event_schedule "
                    f"JOIN users u on u.id_user = list_schedule.id_author "
                    f"JOIN type_event te on e.id_type_event = te.id_type "
                    f"WHERE id_type = {id_type} "
                    f"ORDER BY group_text ASC "
                    f"LIMIT {offset}, 5")
        list_schedule = cur.fetchall()
        cur.close()
        return list_schedule
    except:
        return False


async def db_insert_new_schedule_task(id_event, id_author):
    try:
        cur = conn.cursor()
        data_insert = (id_event, id_author)
        cur.execute(f"INSERT INTO list_schedule(id_event_schedule, id_author) VALUES (?, ?)", data_insert)
        conn.commit()
        cur.close()
    except:
        return False


async def db_remove_schedule_task(id_task):
    try:
        print(id_task)
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute(f"DELETE FROM list_schedule WHERE id_schedule = {id_task}")
        conn.commit()
        cur.close()
    except:
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
                    out_text = out_text + f"{i}. *{task[0]}* \n`назначил: ({task[3]})`\n"

            else:
                out_text = out_text + '-'
    else:
        out_text = 'Список ежедневных задач пуст'

    return out_text
