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
    cur.execute(f"DELETE FROM users WHERE id_user = {user_id};")
    conn.commit()


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

async def db_insert_new_type_task():
    cur = conn.cursor()
    cur.execute()