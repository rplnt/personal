from collections import defaultdict
from pprint import pprint
import multiprocessing
import time

from samesolver import cplay, print_game_stats, get_board, get_hash
from samesolver import get_scores, get_state_count


def fprint(data):
    for line in zip(*data)[::-1]:
        print line
    print


def _get_board():
    return [
        [2, 1, 1, 1, 2],
        [3, 1, 3, 1, 3],
        [3, 2, 3, 1, 4],
        [4, 4, 4, 2, 1],
        [3, 3, 1, 2, 1],
        # [1, 1, 2, 2, 1],
    ]


def main():
    board = get_board()
    fprint(board)

    t0 = time.time()
    try:
        cplay(board)
        print_game_stats()
    except KeyboardInterrupt:
        pass
    t1 = time.time()

    print 'elapsed time: {}'.format(t1-t0)


def loop(count=10):
    score_distribution = defaultdict(int)
    games = []
    try:
        while len(games) < count:
            t = time.time()
            cplay()
            print time.time()-t
            games.append((get_state_count(), (time.time() - t)))
            scores = get_scores()
            for key in scores:
                score_distribution[key] += 1
    except KeyboardInterrupt:
        pass

    for key in sorted(score_distribution, reverse=True):
        print '"{}": "{}",'.format(key, score_distribution[key])

    print 'Avg. time: {}'.format(sum(map(lambda x: x[1], games))/len(games))

    print 'Total game states: {}'.format(sum(map(lambda x: x[0], games)))


class Game(object):
    def __init__(self, game_id=None):
        self.game_id = game_id

    def add_result(self, result_obj):
        self.result_obj = result_obj

    def process(self):
        self.elapsed, self.result = self.result_obj.get(timeout=1)


class Games(object):
    games = {}

    def __init__(self):
        self.created = time.time()

    def __len__(self):
        return len(self.games)

    def __iter__(self):
        for key in self.games:
            yield self.games[key]

    def new_game(self):
        board = get_board()
        board_id = get_hash(board)
        if board_id in self.games:
            print 'Err: duplicit game'
            return self.new_game()

        game = Game(board_id)
        self.games[board_id] = game

        return board_id, board

    def add_result(self, board_id, result_obj):
        if board_id not in self.games:
            return
        self.games[board_id].add_result(result_obj)


def loop_parallel(game_count=10, proc_count=multiprocessing.cpu_count()):
    pool = multiprocessing.Pool(processes=proc_count)
    score_distribution = defaultdict(int)

    print 'Starting {} games, {} in parallel'.format(game_count, proc_count)

    games = Games()
    while len(games) < game_count:
        board_id, board = games.new_game()
        if not board:
            return
        result = pool.apply_async(cplay, (board, 'scores'))
        games.add_result(board_id, result)

    print 'Started {} games, waiting for results...'.format(len(games))

    pool.close()
    pool.join()
    print 'Elapsed time: {:.2f}'.format(time.time() - games.created)
    times = []
    for game in games:
        game.process()
        times.append(game.elapsed)
        for key in game.result:
            score_distribution[key] += 1

    print 'Time: Avg: {:.2f} Max: {:.2f} Min: {:.2f}'.format(sum(times)/len(times), max(times), min(times))

    print 'Score distribution: '
    pprint(dict(score_distribution))


if __name__ == '__main__':
    main()
    # loop()
    # loop_parallel(50)
