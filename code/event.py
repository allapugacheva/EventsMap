from mysql.connector import connect, Error

class Event:

    def __init__(self, name, description, datetime, place, latitude, longitude, organizer = None, load = False):

        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    if organizer:
                        self.name = name
                        self.description = description
                        self.organizer = organizer
                        self.datetime = datetime
                        self.place = place
                        self.latitude = latitude
                        self.longitude = longitude
                        self.visitors = []

                        if load:
                            selectUsersQuery = f""" 
                            SELECT u.name
                            FROM user u
                            JOIN user_event ue ON u.id = ue.user_id
                            WHERE ue.event_id = (SELECT e.id FROM event e WHERE e.name = '{name}');
                            """
                            cursor.execute(selectUsersQuery)
                            users = cursor.fetchall()
                            if users:
                                for user in users:
                                    self.visitors.append(user[0])
                        else:
                            findExitstingEventQuery = f"SELECT COUNT(*) FROM event WHERE name = '{name}'"
                            cursor.execute(findExitstingEventQuery)
                            if cursor.fetchone()[0] > 0:
                                raise ValueError("Событие уже существует")
                            else:
                                createNewEventQuery = f"""
                                INSERT INTO event (name, description, organizer, datetime, place, latitude, longitude)
                                VALUES ("{name}", "{description}", "{organizer}", "{datetime}", "{place}", {latitude}, {longitude})
                                """
                                cursor.execute(createNewEventQuery)
                                connection.commit()
                    else:
                        updateEventQuery = f"""
                        UPDATE event
                        SET name = '{name}',
                            description = '{description}',
                            datetime = '{datetime}',
                            place = '{place}',
                            latitude = {latitude},
                            longitude = {longitude}
                        WHERE name = '{self.name}';
                        """

                        cursor.execute(updateEventQuery)
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

    def add_visitor(self, user):
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
                    user.plannedEvents.append(self.name)
                    
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
