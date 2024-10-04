from mysql.connector import connect, Error

class Event:

    def __init__(self, name, description, datetime, place, latitude, longitude):

        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    update_event_query = f"""
                    UPDATE event
                    SET name = '{name}',
                        description = '{description}',
                        datetime = '{datetime}',
                        place = '{place}',
                        latitude = {latitude},
                        longitude = {longitude}
                    WHERE name = '{self.name}';
                    """

                    cursor.execute(update_event_query)
                    connection.commit()

                    self.name = name
                    self.description = description
                    self.datetime = datetime
                    self.place = place
                    self.latitude = latitude
                    self.longitude = longitude
        except Error:
            raise
        finally:
            connection.close()

    def __init__(self, name, description, organizer, datetime, place, latitude, longitude, load = False):

        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    self.name = name
                    self.description = description
                    self.organizer = organizer
                    self.datetime = datetime
                    self.place = place
                    self.latitude = latitude
                    self.longitude = longitude
                    self.visitors = []

                    if load:

                        select_users_query = f""" 
                        SELECT u.name
                        FROM user u
                        JOIN user_event ue ON u.id = ue.user_id
                        WHERE ue.event_id = (SELECT e.id FROM event e WHERE e.name = '{name}');
                        """
                        cursor.execute(select_users_query)
                        users = cursor.fetchall()
                        if users:
                            for user in users:
                                self.visitors.append(user[0])
                    else:
                        find_exitsting_event_query = f"SELECT COUNT(*) FROM event WHERE name = '{name}'"
                        cursor.execute(find_exitsting_event_query)
                        if cursor.fetchone()[0] > 0:
                            raise ValueError("Событие уже существует")
                        else:
                            create_new_event_query = f"""
                            INSERT INTO event (name, description, organizer, datetime, place, latitude, longitude)
                            VALUES ("{name}", "{description}", "{organizer}", "{datetime}", "{place}", {latitude}, {longitude})
                            """
                            cursor.execute(create_new_event_query)
                            connection.commit()
        except ValueError:
            raise
        except Error:
            raise
        finally:
            connection.close()

    def addVisitor(self, user):
        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    self.visitors.append(user.name)
                    user.plannedEvents.appen(self.name)
                    
                    connect_user_event_query = f"""
                    INSERT INTO user_event (user_id, event_id)
                    SELECT u.id, e.id
                    FROM user u
                    JOIN event e ON u.name = '{user.name}' AND e.name = '{self.name}'
                    """
                    cursor.execute(connect_user_event_query)
                    connection.commit()
        except Error:
            raise
        finally:
            connection.close()
