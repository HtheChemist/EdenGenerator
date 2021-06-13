from eden import Eden
from items import CollectiblesArray, TrinketsArray, PillsArray, CardsArray
from rng import (
    GameSeeds,
    ItemsSeeds,
    PickupSeeds1,
    PickupSeeds2,
    CollectiblesSeeds,
    TrinketsSeeds,
    PillsSeeds,
    CardsSeeds,
)
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

        self.generate_individual_rng()

        self.eden = Eden(self.items_seeds.next(), self.pickup_rng_2, self.verbose)

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

    def print_seed(self):
        print("--- Seed ---")
        print(seed2string(self.seed) + " (" + str(self.seed) + ")")
