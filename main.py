from game import Game
from rng import GameSeeds, DropSeeds, ItemsSeeds
from seeds import seed2string
from pools import ItemType, isaac_items, items_blacklist

verbose_level = 0

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
    collectibles_number = 0x2DA
    
    def __init__(self, active: int = None, passive: int = None, card: int = None, trinket: int = None, start_seed: int = 0):
        self.potential_dropseed = None
        self.start_seed = start_seed
        self.active = active
        self.passive = passive
        self.card = card
        self.trinket = trinket
        self.passive_found = False
        self.active_found = False

    
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


    def check_item_type(self, item_id):
        try:
            return isaac_items[item_id]
        except KeyError:
            return ItemType.Forbidden
   
    def reverse(self):
        while self.start_seed < 0xFFFFFFFF:
            item_id = self.start_seed % self.collectibles_number + 1
            if item_id == self.min_item or item_id == self.max_item:
                if self.check_item_type(item_id) == ItemType.Active:
                    first_item = 'active'
                    self.active_found = True
                else:
                    first_item = 'passive'
                    self.passive_found = True

                print('First item found: ' + str(item_id) + ' (' + first_item + ')')
                self.potential_dropseed = DropSeeds(self.start_seed, 2)
                for i in range(0, 99):
                    item_id = self.potential_dropseed.revese_random(self.collectibles_number) + 1
                    if item_id not in items_blacklist:
                        if self.check_item_type(item_id) == ItemType.Active:
                            if first_item == 'active':
                                print('An active item was found before the right one. Break.')
                                break
                            else:
                                if item_id == self.min_item or item_id == self.max_item:
                                    self.active_found = True
                                    print('The passive and active item are found. Break.')
                                    break
                        elif self.check_item_type(item_id) == ItemType.Passive or self.check_item_type(item_id) == ItemType.Familiar:
                            if first_item == 'passive':
                                print('A passive item was found before the right one. Break.')
                                break
                            else:
                                if item_id == self.min_item or item_id == self.max_item:
                                    self.passive_found = True
                                    print('The passive and active item are found. Break.')
                                    break

                if self.passive_found and self.active_found:
                    print('Going to backtracking')
                    break
            
            print('The two items are not found, resetting.')
            break
            # self.passive_found = False
            # self.active_found = False
            # self.potential_dropseed = None
            # self.start_seed += 1
            
            
        self.potential_dropseed.previous()
        self.generate_different_option()

    @staticmethod
    def from_eden_seed_to_start_seed(seed):
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
    
    def generate_different_option(self):
        # To trinket
        with_trinket_seed = DropSeeds(self.potential_dropseed.seed)
        start_seed = self.from_eden_seed_to_start_seed(with_trinket_seed.previous())
        print('With trinket: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    
        with_card_seed = DropSeeds(self.potential_dropseed.seed)
        card_rng_seed = with_card_seed.previous()
        with_card_seed.previous() & 1
        with_card_seed.previous()
        start_seed = self.from_eden_seed_to_start_seed(with_card_seed.previous())
        print('With card: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    
        with_pill_seed = DropSeeds(self.potential_dropseed.seed)
        pill_rng_seed = with_pill_seed.previous()
        with_pill_seed.previous()
        with_pill_seed.previous()
        start_seed = self.from_eden_seed_to_start_seed(with_pill_seed.previous())
        print('With pill: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
    
        # Bug here
        with_nothing_seed = DropSeeds(self.potential_dropseed.seed,2)
        with_nothing_seed.previous()
        start_seed = self.from_eden_seed_to_start_seed(with_nothing_seed.previous())
        print('With nothing: ' + str(start_seed) + ' (' + seed2string(start_seed) + ')')
        
        
            
    


if __name__ == "__main__":
    reverser = Reverser(active=325, passive=389, start_seed=0xf7a82728)
    reverser.reverse()

    # game = Game(3057554229, 2)
    # game.print_seed()
    # game.eden.print_stats()

# # print('Stage Generation')
# # for stage in stages_seeds:
# #     stage.next() # This one set the stage type
# #     stage.next()
# #     # Missing a lot of these will come back later
# #     # stage.print_seed()
#
#
# verbose = 0
# print('Pill RNG Loop?')
# for var in range(0, 31):
#     pickup_seeds.next()
#     pickup_seeds.next()
# pickup_seeds.genrand(0x270)
# for var in range(0, 12):
#     pickup_seeds.next()
#
#
# print('New some RNG from start seed')
# unknown_seeds_2 = RNG(0x459, [0x3, 0xD, 0x7])
# unknown_seeds_2.next()
# unknown_seeds_2_array = []
# for var in range(0, 0x25): #Pool Seeds?
#     # Pool 0 = Treasure
#     unknown_seeds_2_array.append(RNG(unknown_seeds_2.next(), [0x3, 0xD, 0x7]))
#     unknown_seeds_2_array[var].genrand(0x270)
