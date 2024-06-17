import MySQLdb
import getpass
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates a database and user for MySQL'

    def handle(self, *args, **options):
        # Your logic to create a database user goes here
        root_password = getpass.getpass(prompt="Enter your MySQL root password: ")
        connection = MySQLdb.connect(
            host="localhost",
            port=3306,
            user="root",
            password=root_password
        )

        try:
            cursor = connection.cursor()

            # Check if user 'exidesaftey_user' exists
            cursor.execute("SELECT COUNT(*) FROM mysql.user WHERE user = 'exidesaftey_user' AND host = '%';")
            user_exists = cursor.fetchone()[0]

            if user_exists > 0:
                # Revoke privileges and drop user
                cursor.execute("REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'exidesaftey_user'@'%';")
                cursor.execute("DROP USER 'exidesaftey_user'@'%';")

            # Create user 'exidesaftey_user'
            cursor.execute("CREATE USER 'exidesaftey_user'@'%' IDENTIFIED BY 'exidesaftey_user_password';")

            # Create database 'exidesaftey_db'
            cursor.execute("CREATE DATABASE IF NOT EXISTS exidesaftey_db;")

            # Grant privileges
            cursor.execute("GRANT ALL PRIVILEGES ON exidesaftey_db.* TO 'exidesaftey_user'@'%';")

            # Flush privileges
            cursor.execute("FLUSH PRIVILEGES;")

            self.stdout.write(self.style.SUCCESS("User 'exidesaftey_user' has been granted privileges on database 'exidesaftey_db'."))

        except MySQLdb.Error as error:
            print(f"Error: {error}")

        finally:
            if connection and connection.open:
                connection.close()

        self.stdout.write(self.style.SUCCESS("DB Setup complete."))
        print("Check the MySQLdatabase for the newly added DBs")