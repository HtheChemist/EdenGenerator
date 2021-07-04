from eden import Eden
import numpy as np
from items import CollectiblesArray, TrinketsArray, PillsArray, CardsArray
from rng import (
    GameSeeds,
    ItemsSeeds,
    PickupSeeds1,
    PickupSeeds2,
    CollectiblesSeeds,
    TrinketsSeeds,
    PillsSeeds,
    CardsSeeds, RNG,
)
from pools import pill_colors_number, pill_effects_number
from seeds import seed2string
from stage import World


class Game:
    def __init__(self, seed, verbose):
        self.seed = seed
        self.verbose = verbose
        self.collectibles_seeds = None
        self.trinkets_seeds = None
        self.pills_seeds = None
        self.eden = None

        self.pills_array = np.zeros(13, dtype=int)

        self.game_seeds = GameSeeds(seed, self.verbose)
        self.game_seeds.next()

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Generating Stages"
        if verbose_str:
            print(verbose_str)

        self.world = World(self.game_seeds, self.verbose)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Generating Items RNG"
        if verbose_str:
            print(verbose_str)

        self.items_seeds = ItemsSeeds(self.game_seeds.next(), self.verbose)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Undefined RNG (Placeholder)"
        if verbose_str:
            print(verbose_str)

        self.game_seeds.next()

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "First drop RNG"
        if verbose_str:
            print(verbose_str)

        self.pickup_rng_1 = PickupSeeds1(self.game_seeds.next(), self.verbose)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Second drop RNG (Trinket)"
        if verbose_str:
            print(verbose_str)

        self.pickup_rng_2 = PickupSeeds2(self.pickup_rng_1.next(), self.verbose)

        self.generate_pills_array()
        self.generate_individual_rng()

        self.eden = Eden(self.items_seeds.next(), self.pickup_rng_2, self.pills_array, self.verbose)

    def generate_individual_rng(self):

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Generating Individual Collectible RNG\nCollectibles Seeds"
        if verbose_str:
            print(verbose_str)

        self.collectibles_seeds = CollectiblesArray(
            CollectiblesSeeds(self.items_seeds.next(), self.verbose), self.verbose
        )

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Trinket Seeds"
        if verbose_str:
            print(verbose_str)

        self.trinkets_seeds = TrinketsArray(
            TrinketsSeeds(self.items_seeds.next(), self.verbose), self.verbose
        )

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Pills Seeds"
        if verbose_str:
            print(verbose_str)

        self.pills_seeds = PillsArray(
            PillsSeeds(self.items_seeds.next(), self.verbose), self.verbose
        )

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Cards, Runes and Souls Seeds"
        if verbose_str:
            print(verbose_str)

        self.cards_seeds = CardsArray(
            CardsSeeds(self.items_seeds.next(), self.verbose), self.verbose
        )

    def generate_pills_array(self):
        # This feel hacky as fuck
        # I still can't understand how the effect are given to the pills
        # However, the pills colors order and effect are goods

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Pill Generation Start"
        if verbose_str:
            print(verbose_str)

        verbose_str: str = ""
        if self.verbose > 0:
            verbose_str += "Generation " + str(pill_colors_number+pill_effects_number) + ' Next Random'
        if verbose_str:
            print(verbose_str)

        # I am uncertain what those seeds are used for but they seems to correspond to the the number of pills colors and effects - 1
        for i in range(1, pill_colors_number+pill_effects_number):
            self.pickup_rng_1.next()

        pills_colors = np.arange(0, pill_colors_number, dtype=int)
        pills_effects = np.arange(0, pill_effects_number, dtype=int)
        pills_colors = self.shuffle_array(pills_colors, self.pickup_rng_1)
        pills_effects = self.shuffle_array(pills_effects, self.pickup_rng_1)
        # I think the original code does not remove the 0 since there is a check if the selected index is 0
        pills_effects = pills_effects[pills_effects > 0]
        print(pills_colors+1)
        print(pills_effects)

        for i in pills_colors:
            rnd = self.pickup_rng_1.random(pills_effects.size+1)
            self.pills_array[pills_colors[i]] = pills_effects[rnd]
            pills_effects = np.delete(pills_effects, rnd)

        if self.verbose > 1:
            for index in range(self.pills_array.size):
                print('Color: ' + str(index) + ' - Effect: ' + str(self.pills_array[index]) )

        exit()





    @staticmethod
    def shuffle_array(array: np.ndarray, random: RNG):
        size = array.size
        while size > 1:
            size -= 1
            rnd = random.random(size + 1)
            tmp_val = array[size]
            array[size] = array[rnd]
            array[rnd] = tmp_val

        return array




    def print_seed(self):
        print(seed2string(self.seed) + " (" + str(self.seed) + ")")
