from typing import List, Union

import numpy as np


class RNG:
    # RNG class, so it allows us to get the next or previous number according to their xorshift table.
    # Each RNG object has a different shifts list, and therefore a different xorshift table
    shift: List[int] = [0,0,0]
    seed: int
    old_seed: int
    verbose: int
    random_number: List[int]

    def __init__(self, initial_seed: int, verbose: int = 0):
        if not hasattr(self, "shift"):
            raise AttributeError("Base class cannot be instanced directly")

        self.seed: int = np.uint32(initial_seed)
        self.old_seed: int = 0
        self.verbose: int = verbose
        self.random_numbers: List[int] = []

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "New RNG: " + self.__class__.__name__
        if self.verbose > 1:
            verbose_str += " - Start seed: " + str(hex(self.seed))
        if self.verbose > 3:
            verbose_str += " (" + str(self.seed) + ")"
        if self.verbose > 2:
            verbose_str += " " + str(self.shift)
        if verbose_str:
            print(verbose_str)

    def next(self):
        self.old_seed = self.seed
        self.seed ^= np.uint32(self.seed) >> self.shift[0]
        self.seed ^= np.uint32(self.seed) << self.shift[1]
        self.seed ^= np.uint32(self.seed) >> self.shift[2]
        self.seed = np.uint32(self.seed)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += self.__class__.__name__ + " Next"
        if self.verbose > 1:
            verbose_str += " " + str(hex(self.old_seed)) + " -> " + str(hex(self.seed))
        if self.verbose > 3:
            verbose_str += " (" + str(self.seed) + ")"
        if self.verbose > 2:
            verbose_str += " " + str(self.shift)
        if verbose_str:
            print(verbose_str)

        return self.seed
    
    def previous(self):
        self.old_seed = self.seed
        self.reverse_xor_rshift(self.shift[2])
        self.reverse_xor_lshift(self.shift[1])
        self.reverse_xor_rshift(self.shift[0])
        self.seed = np.uint32(self.seed)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += self.__class__.__name__ + " Previous"
        if self.verbose > 1:
            verbose_str += " " + str(hex(self.old_seed)) + " -> " + str(hex(self.seed))
        if self.verbose > 3:
            verbose_str += " (" + str(self.seed) + ")"
        if self.verbose > 2:
            verbose_str += " " + str(self.shift)
        if verbose_str:
            print(verbose_str)
        
        return self.seed

    def gen_random_array(self, amount_of_number: int):
        self.random_numbers = [self.seed]

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += (
                self.__class__.__name__
                + " Generating "
                + str(amount_of_number)
                + " random number"
            )
        if verbose_str:
            print(verbose_str)

        for i in range(1, amount_of_number):
            self.random_numbers.append(
                np.uint32(
                    i
                    + 0x6C078965
                    * (
                        self.random_numbers[i - 1]
                        ^ (self.random_numbers[i - 1] >> 0x1E)
                    )
                )
            )

            verbose_str: str = ""
            if self.verbose > 4:
                verbose_str += (
                    "Random Number " + str(i) + ": " + str(hex(self.random_numbers[-1]))
                )
            if self.verbose > 5:
                verbose_str += " (" + str(self.random_numbers[-1]) + ")"
            if verbose_str:
                print(verbose_str)

    def reverse_random(self, maximum: int = 1):
        if maximum == 1:
            random_number = self.previous() * 2.3283062e-10
        else:
            random_number = self.previous() % maximum

        verbose_str: str = ""
        if self.verbose > 1:
            verbose_str += "Generated random number: " + str(random_number)
        if self.verbose > 2:
            verbose_str += " (Max: " + str(maximum) + ")"
        if verbose_str:
            print(verbose_str)

        return random_number

    def random(self, maximum: int = None):
        if maximum is None:
            random_number = self.next() * 2.3283062e-10
        else:
            random_number = self.next() % maximum

        verbose_str: str = ""
        if self.verbose > 1:
            verbose_str += "Generated random number: " + str(random_number)
        if self.verbose > 2:
            verbose_str += " (Max: " + str(maximum) + ")"
        if verbose_str:
            print(verbose_str)

        return random_number

    def print_seed(self):
        print(
            "Current Seed: "
            + str(hex(self.seed))
            + " ("
            + str(self.seed)
            + ") "
            + str(self.shift)
        )

    def reverse_xor_lshift(self, shift):
        i = shift
        while i < 32:
            self.seed ^= np.uint32((self.seed << i) & 0xffffffff)
            i *= 2
        self.seed = np.uint32(self.seed)
        #return np.uint32(self.seed)
    
    def reverse_seed(self, w=32):
        self.seed = int(bin(self.seed)[2:].rjust(w, '0')[::-1], 2)

    def reverse_xor_rshift(self, shift):
        self.reverse_seed()
        self.reverse_xor_lshift(shift)
        self.reverse_seed()
        return self.seed
        
        #return self.reverse_bin(self.reverse_xor_lshift(self.reverse_bin(), shift))


class GameSeeds(RNG):
    """
    This RNG is used to generate the root game seed, and is used to generate other RNG
    """

    shift = [0x3, 0x17, 0x19]


class ItemsSeeds(RNG):
    """
    This RNG is used to generate the Pools/ItemsArray seeds
    """

    shift = [0x1, 0xB, 0x10]


class PickupSeeds2(RNG):
    """
    This RNG is used to generate the Seed used in the Get Trinket Algorithm
    """

    shift = [0x1, 0x5, 0x13]


class CollectiblesSeeds(RNG):
    """
    This RNG is used to generate the Collectibles starting seeds
    """

    shift = [0x1, 0x13, 0x3]


class TrinketsSeeds(RNG):
    """
    This RNG is used to generate the Trinkets starting seeds (not the same as the Trinket Pickup Seeds)
    """

    shift = [0x1, 0x15, 0x14]


class PillsSeeds(RNG):
    """
    This RNG is used to generate the Pills starting seeds (not the same as the Pills Generation Seeds)
    """

    shift = [0x1, 0x1B, 0x1B]


class CardsSeeds(RNG):
    """
    This RNG is used to generate the Cards starting seeds
    """

    shift = [0x2, 0x5, 0xF]


class StagesSeeds(RNG):
    """
    This RNG is used to generate the Stage starting seed
    """

    shift = [0x5, 0x9, 0x7]


class StatsSeeds(RNG):
    """
    This RNG is used to generate the Stats (Heart, Key, Bombs, Coins and Attributes) of Eden
    """

    shift = [0x1, 0x5, 0x13]


class DropSeeds(RNG):
    """
    This RNG is used to calculate most of Eden Drop
    """

    shift = [0x1, 0x5, 0x13]


class CardsDrop(RNG):
    """
    This RNG is used to generate the Cards Drop of Eden
    """

    shift = [0x3, 0x3, 0x1D]


class PickupSeeds1(RNG):
    """
    This RNG is used to generate the Pickup and Drop?
    """

    shift = [0x1, 0x9, 0x1D]


class PillsDrop(RNG):
    """
    This RNG is used to generate the Drop for pills
    """

    shift = [0x2, 0x7, 0x9]
