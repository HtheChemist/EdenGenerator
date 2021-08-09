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

verbose_level = 0 # For debugging purpose
num_worker_threads = 10 # Number of CPU
found_seeds = []
thread = [None] * num_worker_threads
instance = [None] * num_worker_threads


def bruteforce(start: int = 0):
    # Not really used mainly for debugging purpose
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
    # This is a non JIT version for development, it is a lot slower than the jit version but it is a bit easier to
    # read and debug

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
        # This is the main reversing algorithm
        print(self.start_seed)
        while self.start_seed < min(0xFFFFFFFF, self.end_seed):
            # It will loop until it reaches the end of its list.
            # print('Trying seed: ' + str(hex(self.start_seed)))
            # Get an item ID from the random number
            # TODO: Skip this if there are not items requested
            item_id = self.start_seed % self.collectibles_number + 1
            # There are not logic to passive/active item numbering so it need to be compared to a set list of values
            # A big of logic is needed to check if it is a passive or active
            if item_id == self.min_item or item_id == self.max_item:
                if self.check_item_type(item_id) == ItemType.Active:
                    first_item_type = self.check_item_type(item_id)
                    self.active_found = True
                else:
                    first_item_type = self.check_item_type(item_id)
                    self.passive_found = True

                # print('First item found: ' + str(item_id) + ' (' + str(first_item_type) + ')')
                # Init an object with the dropseed properties, mainly the xorshift steps.
                self.potential_dropseed = DropSeeds(self.start_seed, 4)

                # The items generation algorithm in the game will do up to 100 try, so we will have the same thing in
                # reverse
                for i in range(0, 99):

                    # Generate a new item id
                    item_id = self.potential_dropseed.reverse_random(self.collectibles_number) + 1

                    # Check if the item id is in the black list, this blacklist is mostly tainted character specific
                    # items or items linked to quest
                    if item_id not in items_blacklist:
                        # Check if it is the same type as the first one. Since we are working in reverse, the new item
                        # will be the one that the game algorithm would have taken, hence invalidating the other item
                        # we will therefore break the loop and go to the next try. Else, we continue the loop.
                        if self.check_item_type(item_id) == first_item_type:
                            # print('Another ' + str(first_item_type) + ' was found before the second one. Break.')
                            break
                        else:
                            # We need to check if the new id is one of interest, if yes, we break our loop, if not we
                            # continue to our next try
                            if item_id == self.min_item or item_id == self.max_item:
                                # print('Second item found: ' + str(item_id))
                                if self.check_item_type(item_id) == ItemType.Active:
                                    self.active_found = True
                                else:
                                    self.passive_found = True
                                break

                # Once we find both item we do the check for the card/trinket/pills
                # TODO:  If no item are specified, the loop should start about here.
                if self.passive_found and self.active_found:

                    # This is used to check what kind of item will be generated.
                    # See here for more explaination: https://bindingofisaacrebirth.fandom.com/wiki/Eden_Generation#Pocket_Items
                    # We reverse generate the 5 potential check (potential maximum), then work from there.
                    # If we find a seed that will gives us the right items, we reverse the seed generation up to the
                    # initial one and add it to the array of found seeds
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

            # We reset the loop and go to the next one
            self.passive_found = False
            self.active_found = False
            self.potential_dropseed = None

            # This part calculated what the next step should be to ensure that the next number will end up with a number
            # that will yield a desired items, this significatively cut down the number of try needed.
            self.start_seed += self.calculate_next_step()

        if self.queue is None:
        #     self.queue.task_done()
        # else:
            for seed in self.found_seed:
                self.print_stats(seed)

    def calculate_next_step(self):
        # This basically ensure that the next modulo will give us an item match
        # TODO: If no item are requeted, step through pocket item number instead
        modulo = self.start_seed % self.collectibles_number
        if modulo + 1 < self.min_item:
            return self.min_item - modulo - 1
        elif self.min_item <= modulo + 1 < self.max_item:
            return self.max_item - modulo - 1
        else:
            return self.collectibles_number - modulo + self.min_item - 1

    def goto_start_seed(self, seed):
        # This will start at the found seed and reverse the Xoshifts up to the initial seed required to get there.
        # See the Game object for more information
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
        # This will generate which trinket will be given for a potential item seed. We need to go back then up since
        # the trinket seed used is generated earlier in the process
        # TODO: Start here for trinket only generation
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
        # Similar to trinket, but we don't need to go as far up
        # The first check is for normal vs special card (runes are ignored)
        if self.potential_holdseed.random(0x19):
            tmp_card = self.potential_holdseed.random(0x16) + 1
            if not self.potential_holdseed.random(7):
                tmp_card += 55
        else:
            # Special card, not implemented
            tmp_card = -1
            pass
        if self.card == tmp_card or self.card == -1:
            return True
        else:
            return False

    def get_pill(self):
        # Not implemented so will always return true
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

    # Uncomment this part to find out what will be Eden stats from a seed number. Note, I do not have implemented the
    # seed code to seed number function, so you need to use an unsigned integer.
    # game = Game(1000,0)

    # This is the main function to find seeds from items value. The main function is jit_reverser, the code before and
    # after is used to split in chunk the script so it can be parallelized.
    # jit_reverse is simply an implementation of the reverse function but with Numba allowed function so it can be
    # compiled and therefore *significatively* sped up.
    ###############
    tasks = []
    seeds = []
    chunk = 100
    completed = 0
    start_time = datetime.now()
    print_progress_bar(completed, chunk)
    with ThreadPoolExecutor(max_workers=num_worker_threads) as executor:
        for i in range(chunk):
            start = i * -(-0xFFFFFFFF//chunk) + 1
            end = (i+1) * -(-0xFFFFFFFF//chunk)
            tasks.append(executor.submit(jit_reverser, active= 352, passive=116, trinket=13, start_seed=start, end_seed=end))
        for task in as_completed(tasks):
            completed += 1
            seeds = seeds + task.result()
            print_progress_bar(completed, chunk)
        end_time = datetime.now()
        print('Completed in: ' + str(end_time - start_time))
        print('Found ' + str(len(seeds)) + ' seeds.')
        for seed in seeds:
            game = Game(seed, 0)
            game.print_seed()
    #########

    # For debug purpose and trying to find seed with a pill
    # for i in range(1000, 2000):
    #     game = Game(i, 0)
    #     if game.eden.pill is not None:
    #         game.print_seed()
    #         game.eden.print_stats()
    #         exit()