from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List

from game import Game
from rng import GameSeeds, DropSeeds, ItemsSeeds, PickupSeeds1, PickupSeeds2, CardsDrop, \
    PillsDrop
from seeds import seed2string
from pools import ItemType, isaac_items, items_blacklist
from queue import Queue
from jitfunctions import jit_reverser

verbose_level = 0
num_worker_threads = 10
found_seeds = []
thread = [None] * num_worker_threads
instance = [None] * num_worker_threads


def bruteforce(start: int = 0):
    # I am at 1561700
    for seed in range(start, 0xFFFFFFFF + 1):
        if not seed % 100:
            print(
                str(seed)
                + "/"
                + str(0xFFFFFFFF)
                + " ("
                + str(round(seed / 0xFFFFFFFF * 100, 3))
                + "%)"
            )
        game = Game(seed, verbose_level)
        # if game.eden.card == 73:
        if (
                game.eden.active == 352
                and game.eden.passive == 432
                and game.eden.card == 73
        ):
            game.print_seed()
            game.eden.print_stats()
            break


class Reverser:

    def __init__(self, active: int = None, passive: int = None, card: int = None, trinket: int = None,
                 pill_effect: int = None, start_seed: int = 0, end_seed: int = 0xFFFFFFFF, seeds: List = None,
                 ref_queue: Queue = None):
        self.collectibles_number: int = 0x2DA
        self.potential_dropseed = None
        self.potential_holdseed = None
        self.potential_trinketseed = None
        self.potential_nothingseed = None
        self.start_seed = start_seed
        self.end_seed = end_seed
        self.active = active
        self.passive = passive
        self.card = card
        self.pill_effect = pill_effect
        self.trinket = trinket
        self.trinket_found = False
        self.passive_found = False
        self.active_found = False
        self.hold_found = False
        self.hold_type = None
        self.hold_seed = None
        self.trinket_seed = None
        self.nothing_seed = None
        self.found_seed = seeds if seeds is not None else []
        self.queue = ref_queue

    @property
    def min_item(self):
        if self.active and self.passive:
            return self.active if self.active < self.passive else self.passive
        elif self.active:
            return self.active
        elif self.passive:
            return self.passive
        else:
            return None

    @property
    def max_item(self):
        if self.active and self.passive:
            return self.active if self.active > self.passive else self.passive
        return None

    @property
    def min_found(self):
        if self.active and self.passive:
            return self.active_found if self.active < self.passive else self.passive_found
        elif self.active:
            return self.active_found
        elif self.passive:
            return self.passive_found
        else:
            return None

    @property
    def max_found(self):
        if self.active and self.passive:
            return self.active_found if self.active > self.passive else self.passive_found
        return None

    @staticmethod
    def check_item_type(item_id):
        item_type = None
        try:
            item_type = isaac_items[item_id]
        except KeyError:
            return ItemType.Forbidden

        if item_type == ItemType.Active:
            return ItemType.Active
        else:
            return ItemType.Passive


    def reverse(self):
        print(self.start_seed)
        while self.start_seed < min(0xFFFFFFFF, self.end_seed):
            # print('Trying seed: ' + str(hex(self.start_seed)))
            item_id = self.start_seed % self.collectibles_number + 1
            if item_id == self.min_item or item_id == self.max_item:
                if self.check_item_type(item_id) == ItemType.Active:
                    first_item_type = self.check_item_type(item_id)
                    self.active_found = True
                else:
                    first_item_type = self.check_item_type(item_id)
                    self.passive_found = True

                # print('First item found: ' + str(item_id) + ' (' + str(first_item_type) + ')')
                self.potential_dropseed = DropSeeds(self.start_seed,4)
                for i in range(0, 99):
                    item_id = self.potential_dropseed.reverse_random(self.collectibles_number) + 1
                    if item_id not in items_blacklist:
                        if self.check_item_type(item_id) == first_item_type:
                            # print('Another ' + str(first_item_type) + ' was found before the second one. Break.')
                            break
                        else:
                            if item_id == self.min_item or item_id == self.max_item:
                                # print('Second item found: ' + str(item_id))
                                if self.check_item_type(item_id) == ItemType.Active:
                                    self.active_found = True
                                else:
                                    self.passive_found = True
                                break

                if self.passive_found and self.active_found:

                    check_point_1 = self.potential_dropseed.previous()
                    check_point_2 = self.potential_dropseed.previous()
                    check_point_3 = self.potential_dropseed.previous()
                    check_point_4 = self.potential_dropseed.previous()
                    check_point_5 = self.potential_dropseed.previous()

                    # Check if with trinket
                    if not check_point_1 % 3 and self.trinket is not None:
                        # print('Trinket possible')
                        self.potential_trinketseed = DropSeeds(check_point_1)
                        if self.get_trinket():
                            self.trinket_seed = self.goto_start_seed(check_point_2)
                            self.print_stats(self.trinket_seed)
                            self.found_seed.append(self.trinket_seed)
                            # break
                        else:
                            # print('This try will not yield the right trinket. Next.')
                            pass
                    elif self.trinket is not None:
                        # print('This try will not yield any trinket. Next')
                        pass

                    # Check if with card or pill
                    if self.card is not None or self.pill_effect is not None:
                        if check_point_2 & 1 and not check_point_3 & 1 and check_point_4 % 3:
                            # print('Pill possible')
                            if self.pill_effect is not None:
                                self.potential_holdseed = PillsDrop(check_point_1)
                                if self.get_pill():
                                    self.hold_seed = self.goto_start_seed(check_point_5)
                                    self.print_stats(self.hold_seed)
                                    self.found_seed.append(self.hold_seed)
                                    # break
                                else:
                                    # print('This try will not yield the right pill. Next.')
                                    pass
                            else:
                                # print('This try will not yield a card. Next.')
                                pass
                        elif not check_point_2 & 1 and not check_point_3 & 1 and check_point_4 % 3:
                            # print('Card possible')
                            if self.card is not None:
                                self.potential_holdseed = CardsDrop(check_point_1)
                                if self.get_card():
                                    self.hold_seed = self.goto_start_seed(check_point_5)
                                    self.print_stats(self.hold_seed)
                                    self.found_seed.append(self.hold_seed)
                                    # break
                                else:
                                    # print('This try will not yield the right card. Next')
                                    pass
                            else:
                                # print('This try will not yield a pill. Next.')
                                pass

                    # Check if it will yield nothing
                    if check_point_1 & 1 and check_point_2 % 3:
                        # print('Theoretically nothing')
                        if self.card is None and self.pill_effect is None and self.trinket is None:
                            self.nothing_seed = self.goto_start_seed(check_point_3)
                            self.print_stats(self.nothing_seed)
                            self.found_seed.append(self.nothing_seed)
                            # break
                        else:
                            # print('This try will yield a pill, card or trinket. Next')
                            pass

            self.passive_found = False
            self.active_found = False
            self.potential_dropseed = None
            self.start_seed += self.calculate_next_step()

        if self.queue is None:
        #     self.queue.task_done()
        # else:
            for seed in self.found_seed:
                self.print_stats(seed)

    def calculate_next_step(self):
        modulo = self.start_seed % self.collectibles_number
        if modulo + 1 < self.min_item:
            return self.min_item - modulo - 1
        elif self.min_item <= modulo + 1 < self.max_item:
            return self.max_item - modulo - 1
        else:
            return self.collectibles_number - modulo + self.min_item - 1

    def goto_start_seed(self, seed):
        items_seeds = ItemsSeeds(seed)
        items_seeds.previous()
        items_seeds.previous()
        items_seeds.previous()
        items_seeds.previous()
        game_seeds = GameSeeds(items_seeds.previous())
        game_seeds.previous()
        for var in range(0, 0xD):
            game_seeds.previous()
        return game_seeds.previous()

    def get_trinket(self):
        self.potential_trinketseed = ItemsSeeds(self.potential_trinketseed.previous())
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed.previous()
        self.potential_trinketseed = GameSeeds(self.potential_trinketseed.previous())
        self.potential_trinketseed.next()
        self.potential_trinketseed = PickupSeeds1(self.potential_trinketseed.next())
        self.potential_trinketseed = PickupSeeds2(self.potential_trinketseed.next())
        trinket_id = self.potential_trinketseed.random(0xBE)
        if trinket_id == self.trinket or self.trinket == -1:
            self.trinket_found = True
            self.trinket = trinket_id
            return True
        else:
            return False

    def get_card(self):
        if self.potential_holdseed.random(0x19):
            tmp_card = self.potential_holdseed.random(0x16) + 1
            if not self.potential_holdseed.random(7):
                tmp_card += 55
        else:
            tmp_card = -1
            pass
        if self.card == tmp_card or self.card == -1:
            return True
        else:
            return False

    def get_pill(self):
        return True

    def print_stats(self, seed):
        print("--- Seed ---")
        print(seed2string(seed) + " (" + str(seed) + ")")
        print("--- Eden ---")
        print("Trinket: " + str(self.trinket))
        print("Card/Soul: " + str(self.card))
        print("Pill: " + str(self.pill_effect))
        print("Active: " + str(self.active))
        print("Passive: " + str(self.passive))


def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

if __name__ == "__main__":
    game = Game(1000,3)

    # tasks = []
    # seeds = []
    # chunk = 100
    # completed = 0
    # start_time = datetime.now()
    # print_progress_bar(completed, chunk)
    # with ThreadPoolExecutor(max_workers=num_worker_threads) as executor:
    #     for i in range(chunk):
    #         start = i * -(-0xFFFFFFFF//chunk) + 1
    #         end = (i+1) * -(-0xFFFFFFFF//chunk)
    #         tasks.append(executor.submit(jit_reverser, active=580, passive=116, trinket=3, start_seed=start, end_seed=end))
    #     for task in as_completed(tasks):
    #         completed += 1
    #         seeds = seeds + task.result()
    #         print_progress_bar(completed, chunk)
    #     end_time = datetime.now()
    #     print('Completed in: ' + str(end_time - start_time))
    #     print('Found ' + str(len(seeds)) + ' seeds.')
    #     for seed in seeds:
    #         game = Game(seed, 0)
    #         game.print_seed()

    # for i in range(1000, 2000):
    #     game = Game(i, 0)
    #     if game.eden.pill is not None:
    #         game.print_seed()
    #         game.eden.print_stats()
    #         exit()