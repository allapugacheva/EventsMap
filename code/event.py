from mysql.connector import connect, Error
import user

class Event:

    def __init__(self, id, name, description, organizer, datetime, city, street, house, latitude, longitude):

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
                    self.city = city
                    self.street = street
                    self.house = house
                    self.latitude = latitude
                    self.longitude = longitude
                    self.visitors = {}

                    if id != 0:
                        self.id = id

                        select_users_query = f""" 
                        SELECT u.iduser, u.name
                        FROM user u
                        JOIN user_event ue ON u.iduser = ue.user
                        WHERE ue.event = '{id}'
                        """
                        cursor.execute(select_users_query)
                        users = cursor.fetchall()
                        if users:
                            for user in users:
                                self.visitors[user[0]] = user[1]
                    else:
                        find_exitsting_event_query = f"SELECT COUNT(*) FROM event WHERE name = '{name}'"
                        cursor.execute(find_exitsting_event_query)
                        if cursor.fetchone()[0] > 0:
                            raise ValueError("Событие уже существует")
                        else:
                            create_new_event_query = f"""
                            INSERT INTO event (name, description, organizer, datetime, city, street, house, latitude, longitude)
                            VALUES ("{name}", "{description}", "{organizer}", "{datetime}", "{city}", "{street}", "{house}", {latitude}, {longitude})
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

                    self.visitors[user.id] = user.name
                    connect_user_event_query = f"""
                    INSERT INYO user_event (user, event)
                    VALUES ({user.id}, {self.id}) 
                    """
                    cursor.execute(connect_user_event_query)
                    connection.commit()
        except Error:
            raise
        finally:
            connection.close()
