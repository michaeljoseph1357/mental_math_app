import random

def generate_addition_problem(difficulty):
    if difficulty == 'easy':
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
    elif difficulty == 'medium':
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
    else:  # hard
        num1 = random.randint(50, 100)
        num2 = random.randint(50, 100)
    
    return num1, num2
