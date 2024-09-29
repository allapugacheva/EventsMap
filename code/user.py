from mysql.connector import connect, Error
from PyQt5.QtWidgets import QMessageBox
import event

class User:

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
                    SELECT u.iduser, u.name, u.password
                    FROM user u
                    WHERE u.name = '{name}'
                    """
                    cursor.execute(select_user_query)
                    user = cursor.fetchone()
                    if user:
                        if password != user[2]:
                            raise ValueError("Неверный пароль")
                        
                        self.id = user[0]
                        self.name = user[1]                        
                        self.plannedEvents = {}

                        events_query = f"""
                        SELECT e.idevent, e.name, e.datetime
                        FROM event e
                        JOIN user_event ue ON e.idevent = ue.event
                        WHERE ue.user = {self.id}
                        """
                        cursor.execute(events_query)
                        events = cursor.fetchall()
                        if events:
                            for event in events:
                                self.plannedEvents[event[0]] = event[1]
                    else:
                        msg_box = QMessageBox()
                        msg_box.setWindowTitle("Профиль не найден")
                        msg_box.setText("Создать новый профиль с указанными данными?")
                        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                        if msg_box.exec_() == QMessageBox.Ok:
                            create_user_query = f"""
                            INSERT INTO user (name, password)
                            VALUES ("{name}","{password}")
                            """
                            with connection.cursor() as cursor:
                                cursor.execute(create_user_query)
                                self.id = cursor.lastrowid
                                self.name = name
                                connection.commit()
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
                    
                    self.plannedEvents[event.id] = event.name
                    connect_user_event_query = f"""
                    INSERT INYO user_event (user, event)
                    VALUES ({self.id}, {event.id})
                    """
                    cursor.execute(connect_user_event_query)
                    connection.commit()
        except Error:
            raise
        finally:
            connection.close()