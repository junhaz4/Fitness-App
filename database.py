import harperdb
import config

db = harperdb.HarperDB(
    url = config.harperdb_url,
    username = config.username,
    password = config.password
)

def insert_workout(workout_id):
    """
    insert one workout data into db
    :param workout_id:
    :return: True or False
    """
    return db.insert(config.schema, config.table, [workout_id])

def delete_workout(workout_id):
    """
    delete one workout data
    :param workout_id:
    :return: True or False
    """
    return db.delete(config.schema, config.table, [workout_id])

def  get_all_workouts():
    """
    :return: all workouts
    """
    try:
        return db.sql(f"select video_id,channel,title,duration from {config.schema}.{config.table}")
    except harperdb.exceptions.HarperDBError:
        return []

def get_daily_workout():
    """
    :return: the first workout_id
    """
    return db.sql(f"select video_id,channel,title,duration from {config.schema}.{config.table} where video_id = 0")

def update_daily_workout(workout_id, insert=False):
    """
    :param workout_id:
    :param insert:
    :return: updated workout_id
    """
    workout_id["id"] = 0
    if insert:
        return db.insert(config.schema, config.daily_table, [workout_id])
    return db.update(config.schema, config.daily_table, [workout_id])

