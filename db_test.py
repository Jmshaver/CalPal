from db import get_db

def db_check():
    connection = get_db()
    users = connection.execute(
        "SELECT * " 
        "FROM users "
    ).fetchall()

    if users:
        for user in users:
            print(user['username'])



if __name__ == "__main__":
  print("hello")
  db_check()
