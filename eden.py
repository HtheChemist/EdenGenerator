from pools import isaac_items, items_blacklist, ItemType
from rng import StatsSeeds, DropSeeds, CardsDrop, PillsDrop


class Eden:
	def __init__(self, eden_seed, pickup_rng, verbose):
		self.verbose = verbose
		
		self.red_hearts = 0
		self.soul_hearts = 0
		
		self.bombs = 0
		self.keys = 0
		self.coins = 0
		
		self.damage_delta = 0
		self.speed_delta = 0
		self.tear_delta = 0
		self.range_delta = 0
		self.shot_speed_delta = 0
		self.luck_delta = 0
		
		self.trinket = None
		self.active = None
		self.passive = None
		self.trinket = None
		self.card = None
		
		self.eden_seed = eden_seed
		self.stats_rng = StatsSeeds(eden_seed, verbose)
		self.drop_rng = DropSeeds(eden_seed, verbose)
		self.cards_rng = None
		self.pills_rng = None
		self.pickup_rng = pickup_rng
		
		self.set_hearts()
		self.set_items()
		self.set_stats()
		self.set_held_item()
		self.set_collectibles()
	
	def print_stats(self):
		print("--- Eden ---")
		print("Red Hearts: " + str(self.red_hearts))
		print("Soul Hearts: " + str(self.soul_hearts))
		print("")
		print("Trinket: " + str(self.trinket))
		print("Card/Soul/Pill: " + str(self.card))
		print("Active: " + str(self.active))
		print("Passive: " + str(self.passive))
		print("")
		print("Damage delta: " + str(self.damage_delta))
		print("Speed delta: " + str(self.speed_delta))
		print("Tear delta: " + str(self.tear_delta))
		print("Range delta: " + str(self.range_delta))
		print("Speed delta: " + str(self.speed_delta))
		print("Luck delta: " + str(self.luck_delta))
	
	def set_hearts(self):
		self.red_hearts = self.stats_rng.next() & 3
		self.soul_hearts = self.stats_rng.random(4 - self.red_hearts)
		
		if self.red_hearts == 0 and self.soul_hearts <= 2:
			self.soul_hearts = 2
	
	def set_items(self):
		if self.stats_rng.random(3):
			if (self.stats_rng.next() & 1) != 0:
				item_selection = self.stats_rng.random(3)
				if item_selection == 0:
					self.coins = self.stats_rng.random(5) + 1
				elif item_selection == 1:
					self.keys = 1
				else:
					self.bombs = self.stats_rng.random(2) + 1
	
	def set_stats(self):
		self.damage_delta = round(self.stats_rng.random() * 2.0 - 1.0, 2)
		self.speed_delta = round(self.stats_rng.random() * 0.30 - 0.15, 2)
		self.tear_delta = round(self.stats_rng.random() * 1.5 - 0.75, 2)
		self.range_delta = round(self.stats_rng.random() * 120.0 - 60, 2)
		self.speed_delta = round(self.stats_rng.random() * 0.5 - 0.25, 2)
		self.luck_delta = round(self.stats_rng.random() * 2.0 - 1.0, 2)
	
	def set_held_item(self):
		if self.drop_rng.random(3):
			if self.drop_rng.next() & 1 == 0:
				if self.drop_rng.next() & 1 == 0:
					# Get Card or Rune
					self.cards_rng = CardsDrop(self.drop_rng.next(), self.verbose)
					if self.cards_rng.random(0x19):
						self.card = self.cards_rng.random(0x16) + 1
						if not self.cards_rng.random(7):
							self.card += 55
					else:
						# Special Card I guess
						pass
				else:
					# Get Pill
					self.pills_rng = PillsDrop(self.drop_rng.next(), self.verbose)
					pill_id = self.pills_rng.random(0xD)
					if not self.pills_rng.random(0x8C):  # Check for Gold Pill
						pill_id = 14
					if not self.pills_rng.random(0x46):  # Check for Horse Pill
						pill_id |= 0x800
		else:
			self.trinket = self.pickup_rng.random(0xBE)

	def set_collectibles(self):
		for var in range(0, 0x64):
			item_id = self.drop_rng.random(0x2DA) + 1
			if item_id in isaac_items:
				if item_id not in items_blacklist:
					if isaac_items[item_id] == ItemType.Active:
						if self.active is None:
							self.active = item_id
					if isaac_items[item_id] == ItemType.Passive:
						if self.passive is None:
							self.passive = item_id
					if isaac_items[item_id] == ItemType.Familiar:
						if self.passive is None:
							self.passive = item_id
			if self.active and self.passive:
				break
