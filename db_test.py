from db import get_db


def db_check():
    connection = get_db()
    try:
        connection.execute(
            "INSERT INTO Food_Intake (USER_ID, Food_name, Calories, Protein, Carbohydrates, Fats) VALUES (1, 'Whole Wheat Pasta with Marinara Sauce', 400, 15, 80, 5)")
    except Exception as e:
        print(f"Error inserting data into database: {e}")

    users = connection.execute(
        "SELECT * "
        "FROM Food_Intake "
    ).fetchall()

    if users:
        for user in users:
            print(user['Food_name'])
    connection.commit()
    connection.close()


if __name__ == "__main__":
    db_check()
