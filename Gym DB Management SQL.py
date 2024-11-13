import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',        
            user='nicholaslord',    
            password='password',
            database='workout'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def add_member(id, name, age):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Members (id, name, age) VALUES (%s, %s, %s)", (id, name, age))
            connection.commit()
            print(f"Member {name} added successfully.")
        except mysql.connector.IntegrityError:
            print("Error: Member ID already exists or is not within constraints.")
        finally:
            cursor.close()
            connection.close()

# Task 2: Add a Workout Session
def add_workout_session(member_id, date, duration_minutes, calories_burned):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Members WHERE id = %s", (member_id,))
            if cursor.fetchone() is None:
                print("Error: Member ID does not exist.")
                return
            
            cursor.execute("INSERT INTO WorkoutSessions (member_id, date, duration_minutes, calories_burned) VALUES (%s, %s, %s, %s)",
                           (member_id, date, duration_minutes, calories_burned))
            connection.commit()
            print("Workout session added successfully.")
        except mysql.connector.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
            connection.close()

# Task 3: Update Member Information
def update_member_age(member_id, new_age):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Members WHERE id = %s", (member_id,))
            if cursor.fetchone() is None:
                print("Error: Member ID does not exist.")
                return
            
            cursor.execute("UPDATE Members SET age = %s WHERE id = %s", (new_age, member_id))
            connection.commit()
            print(f"Member ID {member_id} age updated successfully.")
        except mysql.connector.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
            connection.close()

# Task 4: Delete a Workout Session
def delete_workout_session(session_id):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            if cursor.fetchone() is None:
                print("Error: Session ID does not exist.")
                return

            cursor.execute("DELETE FROM WorkoutSessions WHERE session_id = %s", (session_id,))
            connection.commit()
            print(f"Session ID {session_id} deleted successfully.")
        except mysql.connector.Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
            connection.close()

def get_members_in_age_range(start_age, end_age):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT id, name, age FROM Members WHERE age BETWEEN %s AND %s"
            cursor.execute(query, (start_age, end_age))
            
            # Fetch all results
            results = cursor.fetchall()
            
            # Print each result
            for member in results:
                print(f"ID: {member[0]}, Name: {member[1]}, Age: {member[2]}")
                
            return results
        except Error as e:
            print("Error occurred:", e)
        finally:
            cursor.close()
            connection.close()

get_members_in_age_range(25, 30)  
