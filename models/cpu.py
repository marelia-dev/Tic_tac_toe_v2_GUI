import random
from models.field import Laukas


class CPUZaidejas:
    def __init__(self, mano_simbolis: str, oponento_simbolis: str, level: int = 1, error_rate: float = 0.1):
        self.mano_simbolis = mano_simbolis
        self.oponento_simbolis = oponento_simbolis
        self.level = level
        self.error_rate = error_rate #0.0 - idealus, 0.1 - 10% klaida

        self.vardas = f"CPU {self._level_to_name(level)}"

    def _level_to_name(self, level):
        names = {1: "Lengvas", 2: "Vidutinis", 3: "Sunkus"}
        return names.get(level, "Nezinomas")

    def __str__(self):
        return self.vardas

    def gauti_ejima(self, laukas: Laukas) -> int:
        #grazinam pozicija 1-9
        lentos = laukas.langeliai

        if self.level == 1:
            return self._random_move(lentos)

        elif self.level == 2:
            #tikrinam ar galima laimeti iskart
            win_move = self._find_winning_move(lentos, self.mano_simbolis)
            if win_move is not None:
                return win_move

            #blokuojame oponento laimejima
            block_move = self._find_winning_move(lentos, self.oponento_simbolis)
            if block_move is not None:
                return block_move

            return self._random_move(lentos)

        elif self. level == 3:
            #pilnas minimax
            return self._minimax_best_move(laukas)


    def _random_move(self, lentos: list) -> int:
        free = [i+1 for i, cell in enumerate(lentos) if cell == '  ']
        if not free:
            raise ValueError("Nera laisvu langeliu CPU ejimui")
        return random.choice(free)

    def _find_winning_move(self, lentos: list, sym: str) -> int:
        free = [i for i, cell in enumerate(lentos) if cell == '  ']
        for pos in free:
            temp = lentos[:]
            temp[pos] = sym
            if self._check_win(temp, sym):
                return pos + 1
        return None

    def _check_win(self, board, sym):
        wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for a,b,c in wins:
            if board[a] == sym and board[b] == sym and board[c] == sym:
                return True
        return False

    def _minimax_best_move(self, laukas: Laukas) -> int:
        #randa geriausia ejima Minimax + alpha beta
        board = laukas.langeliai[:]
        best_score = -float('inf')
        best_move = []


        #tikrinam visus tuscius langelius
        for pos in range(9):
            if board[pos] == '  ':  # laisva
                board[pos] = self.mano_simbolis
                score = self._minimax(board, 0, False)  # False = maksimizuojam musu ejima
                board[pos] = '  '  # grazinam

                if score > best_score:
                    best_score = score
                    best_move = [pos + 1]  # 1-9
                elif score == best_score:
                    best_move.append(pos + 1)

        if not best_move:
            #del viso pikto, jei lenta pilna
            return self._random_move(laukas.langeliai)

        ## sprendimas ar zaisti idealiai ar klysti
        if self.level == 3 and random.random() < self.error_rate:
            ## error_rate tikimibe isrenkam ejima is visu laisvu
            free = [i+1 for i, c in enumerate(board) if c == '  ']
            chosen = random.choice(free)
            return chosen
        else:
            #idealus ejimas arba pats geriausias
            chosen = random.choice(best_move)
            return chosen

    def _minimax(self, board: list, depth: int, is_maximizing: bool) -> int:
        """ Rekursinis minimax
        grazina pozicijos ivertinima:
        +10 - mes laimejom
        -10 - priesininkas laimejo
        0 - lygiosios"""

        #tikrinam, ar baigtas zaidimas
        if self._check_win(board, self.mano_simbolis):
            return 10 - depth  # ko greiciau laimejome to geriau
        if self._check_win(board, self.oponento_simbolis):
            return -10 + depth  # ko veliau praleimejome (to geriau mums)
        if '  ' not in board:
            return 0  # lygiosios

        if is_maximizing:
            #musu ejimas maksimizuojam
            max_eval = -float('inf')
            for pos in range(9):
                if board[pos] == '  ':
                    board[pos] = self.mano_simbolis
                    eval = self._minimax(board, depth + 1, False)
                    board[pos] = '  '
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            # priesininko ejimas minimizuojam
            min_eval = float('inf')
            for pos in range(9):
                if board[pos] == '  ':
                    board[pos] = self.oponento_simbolis
                    eval = self._minimax(board, depth + 1, True)
                    board[pos] = '  '
                    min_eval = min(min_eval, eval)
            return min_eval
