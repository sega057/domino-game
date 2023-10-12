from random import randint

MAX_PIECE_VALUE = 6

STATUS_DESCR = {
    'player_move': "Status: It's your turn to make a move. Enter your command.",
    'player_win': 'Status: The game is over. You won!',
    'computer_move': 'Status: Computer is about to make a move. Press Enter to continue...',
    'computer_win': 'Status: The game is over. The computer won!',
    'draw': "Status: The game is over. It's a draw!"
}


class DominoGame:
    def __init__(self):
        self.reshuffle_pieces()
        self.status = 'computer_move' if len(self.computer_pieces) > len(
            self.player_pieces) else 'player_move'

    def get_stock_pieces(self):
        pieces = []

        for i in range(MAX_PIECE_VALUE + 1):
            for j in range(i, MAX_PIECE_VALUE + 1):
                pieces.append([i, j])

        return pieces

    def get_player_pieces(self, stack: list[list]):
        pieces = []

        for _ in range(MAX_PIECE_VALUE + 1):
            index = randint(0, len(stack) - 1)
            piece = stack.pop(index)

            pieces.append(piece)

        return pieces

    def get_domino_snake(self, players: list[list[int]]) -> list[list[int]]:
        highest = -1
        h_player = None
        index = -1

        for player in players:
            for i in range(MAX_PIECE_VALUE + 1):
                first_value, second_value = player[i]
                if first_value != second_value:
                    continue

                if first_value > highest:
                    highest = first_value
                    index = i
                    h_player = player

        if highest < 0:
            self.reshuffle_pieces()
            return None

        h_player.pop(index)
        return [[highest, highest]]

    def reshuffle_pieces(self):
        self.stock_pieces = self.get_stock_pieces()
        self.player_pieces = self.get_player_pieces(self.stock_pieces)
        self.computer_pieces = self.get_player_pieces(self.stock_pieces)
        self.domino_snake = self.get_domino_snake(
            [self.player_pieces, self.computer_pieces])

    def display(self):
        print('=' * 70)
        print('Stock size:', len(self.stock_pieces))
        print('Computer pieces:', len(self.computer_pieces))
        print()

        if len(self.domino_snake) > 6:
            print(*self.domino_snake[:3], sep='', end='')
            print('...', end='')
            print(*self.domino_snake[-3:], sep='')
        else:
            print(*self.domino_snake, sep='')

        print()
        print('Your pieces:')

        for i, piece in enumerate(self.player_pieces):
            print(f'{i + 1}:{piece}')

        print()
        print(STATUS_DESCR[self.status])

    def get_player_move(self):
        while True:
            try:
                move = int(input())
                if abs(move) > len(self.player_pieces):
                    print('Invalid input. Please try again.')
                    continue
                break
            except ValueError:
                print('Invalid input. Please try again.')

        return move

    def make_move(self, pieces: list[list[int]], move: int):
        if move == 0:
            if len(self.stock_pieces) == 0:
                # Skip turn
                return
            index = randint(0, len(self.stock_pieces) - 1)
            pieces.append(self.stock_pieces.pop(index))
            return

        piece = pieces[abs(move) - 1]
        if move > 0:
            end_num = self.domino_snake[-1][1]
            if end_num not in piece:
                raise ValueError()
            if piece[0] != end_num:
                piece.reverse()
            self.domino_snake.append(pieces.pop(abs(move) - 1))
        elif move < 0:
            start_num = self.domino_snake[0][0]
            if start_num not in piece:
                raise ValueError()
            if piece[1] != start_num:
                piece.reverse()
            self.domino_snake.insert(0, pieces.pop(abs(move) - 1))

    def make_player_move(self):
        while True:
            move = self.get_player_move()
            try:
                self.make_move(self.player_pieces, move)
                break
            except ValueError:
                print('Illegal move. Please try again.')

    def make_computer_move(self):
        val_freq = {}

        for piece in self.computer_pieces:
            for value in piece:
                val_freq[value] = val_freq.get(value, 0) + 1

        for piece in self.domino_snake:
            for value in piece:
                val_freq[value] = val_freq.get(value, 0) + 1

        pieces_score = {}
        for i, piece in enumerate(self.computer_pieces):
            pieces_score[i + 1] = val_freq[piece[0]] + val_freq[piece[1]]

        sorted_pieces_score = sorted(
            pieces_score.items(), key=lambda x: x[1], reverse=True)

        for move, _ in sorted_pieces_score:
            try:
                self.make_move(self.computer_pieces, move)
                return
            except ValueError:
                continue

        self.make_move(self.computer_pieces, 0)

    def check_winner(self):
        if len(self.player_pieces) == 0:
            self.status = 'player_win'
        elif len(self.computer_pieces) == 0:
            self.status = 'computer_win'
        elif self.domino_snake[0][0] == self.domino_snake[-1][1]:
            count = 0
            num = self.domino_snake[0][0]

            for piece in self.domino_snake:
                for value in piece:
                    if value == num:
                        count += 1

            if count == 8:
                self.status = 'draw'


domino = DominoGame()

while True:
    domino.display()

    if (domino.status == 'player_win' or
        domino.status == 'computer_win' or
            domino.status == 'draw'):
        break

    if domino.status == 'computer_move':
        input()
        domino.make_computer_move()
        domino.status = 'player_move'
    elif domino.status == 'player_move':
        domino.make_player_move()
        domino.status = 'computer_move'

    domino.check_winner()
