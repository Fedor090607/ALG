import pygame
import random
import math
from queue import PriorityQueue

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 600
GRID_SIZE = 10  
CELL_SIZE = WIDTH // GRID_SIZE
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A*")

# Цвета
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# Типы ячеек
EMPTY = 0
OBSTACLE = 1
START = 2
END = 3
PATH = 4
VISITED = 5

# Класс для одной клетки на поле
class Cell:
    def __init__(self, row, col):
        self.row = row  # строка
        self.col = col  # столбец
        self.x = col * CELL_SIZE  # координаты для рисования в окне
        self.y = row * CELL_SIZE
        self.color = WHITE  # изначально все клетки белые
        self.neighbors = []  # список соседних клеток

    def get_pos(self):
        return self.row, self.col

    # Проверки, какой у клетки сейчас статус по цвету
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == TURQUOISE

    # Функции перекрашивания клетки в нужный цвет
    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = TURQUOISE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_path(self): self.color = PURPLE

    def draw(self, win):
        # Рисуем квадрат ячейки
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Проверяем 4 соседа вокруг (вниз, вверх, вправо, влево), если там нет стены
        if self.row < GRID_SIZE - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < GRID_SIZE - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

# Расчет Манхэттенского расстояния (эвристика h)
def h(p1, p2):
    row1, col1 = p1
    row2, col2 = p2
    return abs(row1 - row2) + abs(col1 - col2)

# Функция восстанавливает путь обратно от финиша к старту
def reconstruct_path(came_from, current, draw_func):
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()  # красим в фиолетовый
        draw_func()

# Алгоритм A*
def a_star_algorithm(draw_func, grid, start, end):
    count = 0
    open_set = PriorityQueue()  # приоритетная очередь для выбора лучшей клетки
    open_set.put((0, count, start))
    came_from = {}  # тут храним историю шагов, чтобы потом восстановить путь
    
    # Изначально все g равны бесконечности
    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0
    
    # Изначально все f равны бесконечности
    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}  # хэш для быстрой проверки, что клетка уже в очереди

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]  # берем узел с самым маленьким f
        open_set_hash.remove(current)

        if current == end:  # если пришли на финиш — строим путь
            reconstruct_path(came_from, end, draw_func)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # шаг на соседа стоит 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()  # красим в зеленый (в очереди)

        draw_func()

        if current != start:
            current.make_closed()  # красим в красный (уже проверено)

    return False

def make_grid():
    grid = []
    for i in range(GRID_SIZE):
        grid.append([])
        for j in range(GRID_SIZE):
            cell = Cell(i, j)
            grid[i].append(cell)
    return grid

def draw_grid(win, grid):
    win.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(win)

    # Рисуем сетку
    for i in range(GRID_SIZE):
        pygame.draw.line(win, GREY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GREY, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH))

    pygame.display.update()

# Мой Вариант 15: расстановка препятствий и точек строго по картинке задания
def setup_variant_15(grid):
    for row in grid:
        for cell in row:
            cell.reset()

    start = grid[0][0]  # Корона на (0,0)
    start.make_start()
    
    end = grid[9][9]  # Крестик на (9,9)
    end.make_end()

    # Списал координаты серых клеток со своей картинки
    barriers = [
        (0, 2), (0, 3), (0, 7), (0, 8),
        (1, 2), (1, 9),
        (2, 0), (2, 2), (2, 4),
        (3, 2), (3, 4), (3, 7),
        (4, 8), (4, 9),
        (5, 1), (5, 4), (5, 5), (5, 6),
        (6, 2),
        (7, 1),
        (8, 2), (8, 7), (8, 8),
        (9, 3), (9, 4), (9, 5)
    ]
    for (row, col) in barriers:
        grid[row][col].make_barrier()

    return start, end

def generate_random_grid(grid):
    # Очищаем сетку
    for row in grid:
        for cell in row:
            cell.reset()

    # Выбираем случайные начальную и конечную точки
    start_row, start_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    # Убедимся, что начальная и конечная точки разные
    while (start_row, start_col) == (end_row, end_col):
        end_row, end_col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)

    start = grid[start_row][start_col]
    end = grid[end_row][end_col]

    start.make_start()
    end.make_end()

    # Добавляем случайные препятствия (20% ячеек)
    obstacle_count = int(GRID_SIZE * GRID_SIZE * 0.2)
    for _ in range(obstacle_count):
        row, col = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        cell = grid[row][col]
        if not cell.is_start() and not cell.is_end():
            cell.make_barrier()

    return start, end

def main():
    grid = make_grid()
    # При запуске сначала грузится карта моего 15 варианта
    start, end = setup_variant_15(grid)
    run = True

    while run:
        draw_grid(WIN, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # Нажмите SPACE, чтобы запустить алгоритм A*
                if event.key == pygame.K_SPACE:  
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    a_star_algorithm(lambda: draw_grid(WIN, grid), grid, start, end)

                # Нажмите R, чтобы сгенерировать новое случайное поле
                if event.key == pygame.K_r:  
                    start, end = generate_random_grid(grid)

                # Добавил кнопку V, чтобы быстро возвращать сетку своего варианта
                if event.key == pygame.K_v:  
                    start, end = setup_variant_15(grid)

    pygame.quit()

main()
