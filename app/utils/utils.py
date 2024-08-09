import random

def generate_problem(difficulty, game_type):
    if difficulty == 'easy':
        num1, num2 = random.randint(1, 12), random.randint(1, 12)
    elif difficulty == 'medium':
        num1, num2 = random.randint(12, 99), random.randint(12, 99)
    elif difficulty == 'hard':
        num1, num2 = random.randint(101, 999), random.randint(101, 999)

    # Adjust for subtraction to avoid negative results
    if game_type == 'subtraction':
        if num1 < num2:
            num1, num2 = num2, num1

    # Adjust for division to avoid results less than 1
    if game_type == 'division':
        num1 = num1 * num2  # Ensure num1 is a multiple of num2, may need to revisit this depending on difficulty

    return num1, num2
