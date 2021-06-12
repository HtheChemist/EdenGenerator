from game import Game
from seeds import seed2string

verbose_level = 0

if __name__ == "__main__":
	for seed in range(0, 0xFFFFFFFF):
		if not seed % 100:
			print(str(seed) + '/' + str(0xFFFFFFFF) + ' (' + str(round(seed/0xFFFFFFFF*100,3)) + '%)' )
		game = Game(seed, verbose_level)
		#if game.eden.card == 73:
		if game.eden.active == 352 and game.eden.passive == 432 and game.eden.card == 73:
			game.print_seed()
			game.eden.print_stats()
			break

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
