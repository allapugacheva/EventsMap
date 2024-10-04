from mysql.connector import connect, Error
from PyQt5.QtWidgets import QMessageBox

class User:

    def __init__(self, name, password, defaultLatitude, defaultLongitude):
        
        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    select_user_query = f""" 
                    SELECT u.name
                    FROM user u
                    WHERE u.name = '{name}'
                    """
                    cursor.execute(select_user_query)
                    user = cursor.fetchone()
                    if user:
                        raise ValueError("Такой пользователь уже существует")
                    else:
                        create_user_query = f"""
                        INSERT INTO user (name, password, defaultLatitude, defaultLongitude)
                        VALUES ("{name}","{password}", {defaultLatitude}, {defaultLongitude})
                        """
                        with connection.cursor() as cursor:
                            cursor.execute(create_user_query)
                            self.name = name
                            self.defaultLatitude = defaultLatitude
                            self.defaultLongitude = defaultLongitude
                            connection.commit()
        except ValueError:
            raise
        except Error:
            raise
        finally:
            connection.close()

    def __init__(self, name, password):
        
        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:

                    select_user_query = f""" 
                    SELECT u.id, u.name, u.password, u.defaultLatitude, u.defaultLongitude
                    FROM user u
                    WHERE u.name = '{name}'
                    """
                    cursor.execute(select_user_query)
                    user = cursor.fetchone()
                    if user:
                        if password != user[2]:
                            raise ValueError("Неверный пароль")
                        
                        self.name = user[1]  
                        self.defaultLatitude = user[3]
                        self.defaultLongitude = user[4]                      
                        self.plannedEvents = []

                        events_query = f"""
                        SELECT e.name
                        FROM event e
                        JOIN user_event ue ON e.id = ue.event_id
                        WHERE ue.user_id = {user[0]}
                        """
                        cursor.execute(events_query)
                        events = cursor.fetchall()
                        if events:
                            for event in events:
                                self.plannedEvents.append(event[0])
                    else:
                        raise ValueError("Такой пользователь не найден")
        except ValueError:
            raise
        except Error:
            raise
        finally:
            connection.close()

    def addEvent(self, event):
        try:
            with connect(
                host="localhost",
                user="root",
                password="13579",
                port="3307",
                database="eventsmapdb"
            ) as connection:
                with connection.cursor() as cursor:
                    
                    self.plannedEvents.append(event.name)
                    event.visitors.append(self.name)
                    
                    connect_user_event_query = f"""
                    INSERT INTO user_event (user_id, event_id)
                    SELECT u.id, e.id
                    FROM user u
                    JOIN event e ON u.name = '{self.name}' AND e.name = '{event.name}'
                    """
                    cursor.execute(connect_user_event_query)
                    connection.commit()
        except Error:
            raise
        finally:
            connection.close()