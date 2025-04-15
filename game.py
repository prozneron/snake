import random
import json
import time

class SnakeGame:
    def __init__(self, settings):
        self.width = 50
        self.height = 50
        self.settings = settings
        self.speed_map = {
            'slow': 0.3,
            'normal': 0.2,
            'fast': 0.1
        }
        self.last_move_time = time.time()
        self.reset_game()

    def reset_game(self):
        self.snake = [(self.width // 2, self.height // 2)]
        self.direction = 'right'
        self.food = self.generate_food()
        self.score = 0
        self.lives = self.settings['lives']
        self.game_over = False
        self.paused = False
        self.last_move_time = time.time()

    def generate_food(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if (x, y) not in self.snake:
                return (x, y)

    def move(self, direction=None):
        if self.game_over or self.paused:
            return

        current_time = time.time()
        if current_time - self.last_move_time < self.speed_map[self.settings.get('speed', 'normal')]:
            return

        if direction in ['up', 'down', 'left', 'right']:
            # Prevent 180-degree turns
            if (direction == 'up' and self.direction != 'down') or \
               (direction == 'down' and self.direction != 'up') or \
               (direction == 'left' and self.direction != 'right') or \
               (direction == 'right' and self.direction != 'left'):
                self.direction = direction

        head = self.snake[0]
        if self.direction == 'up':
            new_head = (head[0], head[1] - 1)
        elif self.direction == 'down':
            new_head = (head[0], head[1] + 1)
        elif self.direction == 'left':
            new_head = (head[0] - 1, head[1])
        else:  # right
            new_head = (head[0] + 1, head[1])

        # Check borders
        if self.settings['borders'] == 'kills':
            if (new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.reset_game()
                return
        else:  # teleport
            # Handle left border
            if new_head[0] < 0:
                new_head = (self.width - 1, new_head[1])
            # Handle right border
            elif new_head[0] >= self.width:
                new_head = (0, new_head[1])
            # Handle top border
            elif new_head[1] < 0:
                new_head = (new_head[0], self.height - 1)
            # Handle bottom border
            elif new_head[1] >= self.height:
                new_head = (new_head[0], 0)

        # Check self collision
        if new_head in self.snake:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.reset_game()
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.last_move_time = current_time

    def get_state(self):
        board = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw borders
        for i in range(self.width):
            board[0][i] = '-'
            board[self.height-1][i] = '-'
        for i in range(self.height):
            board[i][0] = '|'
            board[i][self.width-1] = '|'

        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            board[y][x] = 'O' if i == 0 else '#'

        # Draw food
        board[self.food[1]][self.food[0]] = '+'

        # Add game info at the top of the board
        high_score = self.settings.get('high_score', 0)
        info_text = f"Lives:{self.lives} Score:{self.score} High:{high_score}"
        for i, char in enumerate(info_text):
            if i < self.width - 2:  # Ensure we don't exceed board width
                board[0][i+1] = char

        return {
            'board': board,
            'score': self.score,
            'lives': self.lives,
            'game_over': self.game_over,
            'paused': self.paused,
            'high_score': high_score
        } 