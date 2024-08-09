import random

def generate_problem(difficulty):
    if difficulty == 'easy':
        return random.randint(1, 10), random.randint(1, 10)
    elif difficulty == 'medium':
        return random.randint(10, 100), random.randint(10, 100)
    elif difficulty == 'hard':
        return random.randint(100, 1000), random.randint(100, 1000)
    else:
        return 0, 0  # Fallback case
