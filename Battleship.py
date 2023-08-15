from random import randint


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return f'Вы стреляете за границы доски'


class BoardUserException(BoardException):
    def __str__(self):
        return f'Вы уже стреляли в эту клетку'


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'({self.x};{self.y})'


class Ship:
    def __init__(self, bow, long, rotation,):
        self.bow = bow
        self.long = long
        self.rotation = rotation
        self.hp = long

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.long):
            cour_x = self.bow.x
            cour_y = self.bow.y

            if self.rotation == 0:
                cour_x += i
            elif self.rotation == 1:
                cour_y += i

            ship_dots.append(Dot(cour_x, cour_y))
        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.field = [["0"] * size for _ in range(size)]
        self.ships = []
        self.busy = []
        self.hid = hid
        self.size = size
        self.count = 0

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "#"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cour = Dot(d.x + dx, d.y + dy)
                if not(self.out(cour)) and cour not in self.busy:
                    if verb:
                        self.field[cour.x][cour.y] = '.'
                    self.busy.append(cour)

    def __str__(self):
        res = ''
        res += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            res += f"\n{i+1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace('#', '0')
        return res

    def out(self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUserException()
        self.busy.append(d)
        for ship in self.ships:
            if d in ship.dots:
                ship.hp -= 1
                self.field[d.x][d.y] = 'X'
                if ship.hp == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print('Корабль уничтожен!')
                    return True
                else:
                    print('Корабль ранен!')
                    return True
        self.field[d.x][d.y] = '.'
        print('Мимо!')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x+1} {d.y+1}')
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()
            if len(cords) != 2:
                print(' Введите 2 координаты!')
                continue

            x, y = cords

            if not(x.isdigit()) or not (y.isdigit()):
                print('Введите числа!')
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)


class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    @staticmethod
    def hstack(first, second):
        first_sp = first.split("\n")
        second_sp = second.split("\n")
        max_width = max(map(len, first_sp))
        max_len = max(len(first_sp), len(second_sp))
        first_sp += [""] * (max_len - len(first_sp))
        second_sp += [""] * (max_len - len(second_sp))
        text = []
        for f, s in zip(first_sp, second_sp):
            text.append(f"{f: <{max_width}}   |:|   {s: <{max_width}}")

        return "\n".join(text)

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for ln in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), ln, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):
        print('-----------------')
        print(' Приветствую вас ')
        print('     в игре      ')
        print('   Морской Бой   ')
        print('-----------------')
        print('формат ввода: x y')
        print('x - номер строки ')
        print('y - номер столбца')

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            user_board = "Доска пользователя:\n\n" + str(self.us.board)
            ai_board = "Доска компьютера:\n\n" + str(self.ai.board)
            print(self.hstack(user_board, ai_board))
            if num % 2 == 0:
                print('-'*20)
                print('Ходит пользователь!')
                repeat = self.us.move()
            else:
                print('-' * 20)
                print('Ходит компьютер!')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('-' * 20)
                user_board = "Доска пользователя:\n\n" + str(self.us.board)
                ai_board = "Доска компьютера:\n\n" + str(self.ai.board)
                print(self.hstack(user_board, ai_board))
                print('-' * 20)
                print('Пользователь выиграл!')
                break

            if self.us.board.count == 7:
                print('-' * 20)
                user_board = "Доска пользователя:\n\n" + str(self.us.board)
                ai_board = "Доска компьютера:\n\n" + str(self.ai.board)
                print(self.hstack(user_board, ai_board))
                print('-' * 20)
                print('Компьютер выиграл!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()