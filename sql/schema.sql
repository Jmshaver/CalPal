PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS Food_Intake;
CREATE TABLE users(
  USER_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  First_name VARCHAR(40) NOT NULL,
  Last_name VARCHAR(40) NOT NULL,
  Height INTEGER NOT NULL,
  Starting_Weight INT NOT NULL,
  Age INT NOT NULL,
  Activity_type VARCHAR(50) NOT NULL CHECK (
    Activity_type IN (
      'SEDENTARY',
      'LIGHT',
      'MODERATE',
      'VERY',
      'EXTREMELY'
    )
  ),
  Sex VARCHAR(6) NOT NULL CHECK (Sex IN ('male', 'female', 'other')),
  Calorie_goal INTEGER NOT NULL,
  Diet_type VARCHAR(50) NOT NULL CHECK (
    Diet_type IN (
      'BALANCED',
      'HIGH PROTEIN',
      'LOW CARB'
    )
  ),
  Protein_goal INTEGER NOT NULL,
  Fat_goal INTEGER NOT NULL,
  Carb_goal INTEGER NOT NULL,
  UNIQUE(First_name, Last_name)
);
CREATE TABLE Food_Intake(
  Intake_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  USER_ID INTEGER NOT NULL,
  CREATED DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
  Food_name VARCHAR(50) NOT NULL,
  Calories FLOAT NOT NULL,
  Protein FLOAT NOT NULL,
  Carbohydrates FLOAT NOT NULL,
  Fats FLOAT NOT NULL,
  FOREIGN KEY(user_id) REFERENCES users(USER_ID)
);