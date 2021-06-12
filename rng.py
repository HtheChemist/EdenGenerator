from typing import List, Union

import numpy as np


class RNG:
    shift: List[int]
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

    def random(self, maximum: int = 1):
        random_number: Union[int, float] = 0
        if maximum == 1:
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