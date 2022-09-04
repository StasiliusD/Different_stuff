"""Необходимо объявить класс с именем TicTacToe (крестики-нолики) для управления игровым процессом. Объекты этого класса будут создаваться командой:

game = TicTacToe()
В каждом объекте этого класса должен быть публичный атрибут:

pole - двумерный кортеж, размером 3x3.

Каждый элемент кортежа pole является объектом класса Cell:

cell = Cell()
В объектах этого класса должно автоматически формироваться локальное свойство:

value - текущее значение в ячейке: 0 - клетка свободна; 1 - стоит крестик; 2 - стоит нолик.

Также с объектами класса Cell должна выполняться функция:

bool(cell) - возвращает True, если клетка свободна (value = 0) и False - в противном случае.

К каждой клетке игрового поля должен быть доступ через операторы:

res = game[i, j] # получение значения из клетки с индексами i, j
game[i, j] = value # запись нового значения в клетку с индексами i, j
Если индексы указаны неверно (не целые числа или числа, выходящие за диапазон [0; 2]), то следует генерировать исключение командой:

raise IndexError('некорректно указанные индексы')
Чтобы в программе не оперировать величинами: 0 - свободная клетка; 1 - крестики и 2 - нолики, в классе TicTacToe должны быть три публичных атрибута (атрибуты класса):

FREE_CELL = 0      # свободная клетка
HUMAN_X = 1        # крестик (игрок - человек)
COMPUTER_O = 2     # нолик (игрок - компьютер)
В самом классе TicTacToe должны быть объявлены следующие методы (как минимум):

init() - инициализация игры (очистка игрового поля, возможно, еще какие-либо действия);
show() - отображение текущего состояния игрового поля (как именно - на свое усмотрение);
human_go() - реализация хода игрока (запрашивает координаты свободной клетки и ставит туда крестик);
computer_go() - реализация хода компьютера (ставит случайным образом нолик в свободную клетку).

Также в классе TicTacToe должны быть следующие объекты-свойства (property):

is_human_win - возвращает True, если победил человек, иначе - False;
is_computer_win - возвращает True, если победил компьютер, иначе - False;
is_draw - возвращает True, если ничья, иначе - False.

Наконец, с объектами класса TicTacToe должна выполняться функция:

bool(game) - возвращает True, если игра не окончена (никто не победил и есть свободные клетки) и False - в противном случае.

Все эти функции и свойства предполагается использовать следующим образом (эти строчки в программе не писать):

game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
Вам в программе необходимо объявить только два класса: TicTacToe и Cell так, чтобы с их помощью можно было бы сыграть в "Крестики-нолики" между человеком и компьютером.

P.S. Запускать игру и выводить что-либо на экран не нужно. Только объявить классы."""
import random


class TicTacToe:
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))

    def check_index(self, index):
        r, c = index
        if not type(r) == int or not type(r) == int or r not in (0, 1, 2) or c not in (0, 1, 2):
            raise IndexError('некорректно указанные индексы')

    def init(self):
        for r in range(3):
            for c in range(3):
                self.pole[r][c].value = 0

    #        setattr(self, 'is_human_win', False)
    #        setattr(self, 'is_computer_win', False)
    #        setattr(self, 'is_draw', False)
    #        self.is_human_win = False
    #        self.is_computer_win = False
    #        self.is_draw = False

    def __bool__(self):
        free_cells = []
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == 0:
                    free_cells.append(self.pole[i][j])
        if len(free_cells) > 0 and not getattr(self, 'is_human_win') and not getattr(self,
                                                                                     'is_computer_win') and not getattr(
                self, 'is_draw'):
            return True
        else:
            return False

    def show(self):
        for i in range(3):
            for j in range(3):
                print(self.pole[i][j].value)
        print()

    def __getitem__(self, item):
        self.check_index(item)
        r, c = item
        return self.pole[r][c].value

    def __setitem__(self, item, value):
        self.check_index(item)
        r, c = item
        self.pole[r][c].value = value

    def human_go(self):
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == 0:
                    self.pole[i][j].value = 1
                    break

    def computer_go(self):
        free_cells = []
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == 0:
                    free_cells.append(self.pole[i][j])
        k = random.choice(free_cells)
        k.value = 2

    @property
    def is_human_win(self):
        return (self.pole[0][0].value == self.pole[0][1].value == self.pole[0][2].value == 1) or (
                    self.pole[1][0].value == self.pole[1][1].value == self.pole[1][2].value == 1) or (
                           self.pole[2][0].value == self.pole[2][1].value == self.pole[2][2].value == 1) or (
                           self.pole[0][0].value == self.pole[1][0].value == self.pole[2][0].value == 1) or (
                           self.pole[0][1].value == self.pole[1][1].value == self.pole[2][1].value == 1) or (
                           self.pole[0][2].value == self.pole[1][2].value == self.pole[2][2].value == 1) or (
                           self.pole[0][0].value == self.pole[1][1].value == self.pole[2][2].value == 1) or (
                           self.pole[0][2].value == self.pole[1][1].value == self.pole[2][0].value == 1)

    #    @is_human_win.setter
    #    def is_human_win(self, value):
    #        self.is_human_win = value

    @property
    def is_computer_win(self):
        return (self.pole[0][0].value == self.pole[0][1].value == self.pole[0][2].value == 2) or (
                    self.pole[1][0].value == self.pole[1][1].value == self.pole[1][2].value == 2) or (
                           self.pole[2][0].value == self.pole[2][1].value == self.pole[2][2].value == 2) or (
                           self.pole[0][0].value == self.pole[1][0].value == self.pole[2][0].value == 2) or (
                           self.pole[0][1].value == self.pole[1][1].value == self.pole[2][1].value == 2) or (
                           self.pole[0][2].value == self.pole[1][2].value == self.pole[2][2].value == 2) or (
                           self.pole[0][0].value == self.pole[1][1].value == self.pole[2][2].value == 2) or (
                           self.pole[0][2].value == self.pole[1][1].value == self.pole[2][0].value == 2)

    #    @is_computer_win.setter
    #    def is_computer_win(self, value):
    #        self.is_computer_win = value

    @property
    def is_draw(self):
        free_cells = []
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].value == 0:
                    free_cells.append(self.pole[i][j])
        return len(free_cells) == 0 and not getattr(self, 'is_human_win') and not getattr(self, 'is_computer_win')


#    @is_draw.setter
#    def is_draw(self, value):
#        self.is_draw = value

class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        if self.value == 0:
            return True
        else:
            return False
cell = Cell()
assert cell.value == 0, "начальное значение атрибута value объекта класса Cell должно быть равно 0"
assert bool(cell), "функция bool для объекта класса Cell вернула неверное значение"
cell.value = 1
assert bool(cell) == False, "функция bool для объекта класса Cell вернула неверное значение"

assert hasattr(TicTacToe, 'show') and hasattr(TicTacToe, 'human_go') and hasattr(TicTacToe, 'computer_go'), "класс TicTacToe должен иметь методы show, human_go, computer_go"

game = TicTacToe()
assert bool(game), "функция bool вернула неверное значения для объекта класса TicTacToe"
assert game[0, 0] == 0 and game[2, 2] == 0, "неверные значения ячеек, взятые по индексам"
game[1, 1] = TicTacToe.HUMAN_X
assert game[1, 1] == TicTacToe.HUMAN_X, "неверно работает оператор присваивания нового значения в ячейку игрового поля"

game[0, 0] = TicTacToe.COMPUTER_O
assert game[0, 0] == TicTacToe.COMPUTER_O, "неверно работает оператор присваивания нового значения в ячейку игрового поля"

game.init()
assert game[0, 0] == TicTacToe.FREE_CELL and game[1, 1] == TicTacToe.FREE_CELL, "при инициализации игрового поля все клетки должны принимать значение из атрибута FREE_CELL"

try:
    game[3, 0] = 4
except IndexError:
    assert True
else:
    assert False, "не сгенерировалось исключение IndexError"

game.init()
assert game.is_human_win == False and game.is_computer_win == False and game.is_draw == False, "при инициализации игры атрибуты is_human_win, is_computer_win, is_draw должны быть равны False, возможно не пересчитывается статус игры при вызове метода init()"

game[0, 0] = TicTacToe.HUMAN_X
game[1, 1] = TicTacToe.HUMAN_X
game[2, 2] = TicTacToe.HUMAN_X
assert game.is_human_win and game.is_computer_win == False and game.is_draw == False, "некорректно пересчитываются атрибуты is_human_win, is_computer_win, is_draw. Возможно не пересчитывается статус игры в момент присвоения новых значения по индексам: game[i, j] = value"

game.init()
game[0, 0] = TicTacToe.COMPUTER_O
game[1, 0] = TicTacToe.COMPUTER_O
game[2, 0] = TicTacToe.COMPUTER_O
assert game.is_human_win == False and game.is_computer_win and game.is_draw == False, "некорректно пересчитываются атрибуты is_human_win, is_computer_win, is_draw. Возможно не пересчитывается статус игры в момент присвоения новых значения по индексам: game[i, j] = value"