PRAGMA foreign_keys = ON;
INSERT INTO users (
    First_name,
    Last_name,
    Height,
    Starting_Weight,
    Activity_type,
    Sex,
    Calorie_goal,
    Age,
    Diet_type,
    Protein_goal,
    Fat_goal,
    Carb_goal
  )
VALUES (
    'Jay',
    'S',
    72,
    180,
    'SEDENTARY',
    'male',
    3000,
    15,
    "BALANCED",
    117,
    100,
    408
  );
INSERT INTO Food_Intake(
    USER_ID,
    Food_name,
    Calories,
    Protein,
    Carbohydrates,
    Fats
  )
VALUES (1, 'Grilled Chicken Salad', 350, 25, 10, 20);
INSERT INTO Food_Intake(
    USER_ID,
    Food_name,
    Calories,
    Protein,
    Carbohydrates,
    Fats
  )
VALUES (
    1,
    'Whole Wheat Pasta with Marinara Sauce',
    400,
    15,
    80,
    5
  );