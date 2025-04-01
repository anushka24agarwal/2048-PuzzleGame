import time
import math
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        start_time = time.time()
        depth_limit = 4
        _, move = self.expectiminimax(grid, depth_limit, float('-inf'), float('inf'), True, start_time)
        return move[0]

    def expectiminimax(self, grid, depth, alpha, beta, maximizing_player, start_time):
        if depth == 0 or time.time() - start_time > 0.19:
            return self.evaluate(grid), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            moves = grid.getAvailableMoves()
            moves.sort(key=lambda x: self.move_ordering_heuristic(grid, x), reverse=True)

            for move in moves:
                new_grid = grid.clone()
                new_grid.move(move)
                eval, _ = self.expectiminimax(new_grid, depth - 1, alpha, beta, False, start_time)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        else:  # Chance node (computer's turn)
            avg_eval = 0
            empty_cells = grid.getAvailableCells()
            num_empty = len(empty_cells)

            for cell in empty_cells:
                new_grid = grid.clone()
                new_grid.setCellValue(cell, 2)  # 90% chance of 2
                eval, _ = self.expectiminimax(new_grid, depth - 1, alpha, beta, True, start_time)
                avg_eval += 0.9 * eval / num_empty

                new_grid = grid.clone()
                new_grid.setCellValue(cell, 4)  # 10% chance of 4
                eval, _ = self.expectiminimax(new_grid, depth - 1, alpha, beta, True, start_time)
                avg_eval += 0.1 * eval / num_empty

            return avg_eval, None

    def evaluate(self, grid):
        weights = {
            'empty_cells': 10,
            'max_value': 1,
            'smoothness': 1,
            'monotonicity': 2,
            'corner_max': 5
        }

        empty_cells = len(grid.getAvailableCells())
        max_value = grid.getMaxTile()
        smoothness = self.get_smoothness(grid)
        monotonicity = self.get_monotonicity(grid)
        corner_max = self.get_corner_max(grid)

        score = (weights['empty_cells'] * empty_cells +
                 weights['max_value'] * math.log2(max_value) +
                 weights['smoothness'] * smoothness +
                 weights['monotonicity'] * monotonicity +
                 weights['corner_max'] * corner_max)

        return score

    def get_smoothness(self, grid):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                if j < 3 and grid.map[i][j] != 0:
                    smoothness -= abs(math.log2(grid.map[i][j]) - math.log2(max(grid.map[i][j+1], 1)))
                if i < 3 and grid.map[i][j] != 0:
                    smoothness -= abs(math.log2(grid.map[i][j]) - math.log2(max(grid.map[i+1][j], 1)))
        return smoothness

    def get_monotonicity(self, grid):
        totals = [0, 0, 0, 0]

        for i in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[i][next] == 0:
                    next += 1
                if next >= 4:
                    next -= 1
                current_value = math.log2(grid.map[i][current]) if grid.map[i][current] != 0 else 0
                next_value = math.log2(grid.map[i][next]) if grid.map[i][next] != 0 else 0
                if current_value > next_value:
                    totals[0] += next_value - current_value
                elif next_value > current_value:
                    totals[1] += current_value - next_value
                current = next
                next += 1

        for j in range(4):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[next][j] == 0:
                    next += 1
                if next >= 4:
                    next -= 1
                current_value = math.log2(grid.map[current][j]) if grid.map[current][j] != 0 else 0
                next_value = math.log2(grid.map[next][j]) if grid.map[next][j] != 0 else 0
                if current_value > next_value:
                    totals[2] += next_value - current_value
                elif next_value > current_value:
                    totals[3] += current_value - next_value
                current = next
                next += 1

        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    def get_corner_max(self, grid):
        corners = [grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]]
        return max(corners) == grid.getMaxTile()

    def move_ordering_heuristic(self, grid, move):
        new_grid = grid.clone()
        new_grid.move(move)
        return self.evaluate(new_grid)
