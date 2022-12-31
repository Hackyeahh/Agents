import itertools
from abc import ABC, abstractmethod
import random
from collections import deque


class BaseCard(ABC):
	def __init__(self, **child_args):
		self.name = child_args.get('name', '<blank card>')
		self.energy_cost = child_args.get('energy_cost', 1)
		self.priority = child_args.get('priority', 50)

	def query(self, **child_args):
		"""Get necessary information to be asked and stored in the Card object.
		information is then used later on in execute()."""
		return

	def can_execute(self, **child_args):
		return True

	@abstractmethod
	def execute(self, caster, target):
		"""Running this activates the default card behaviour."""
		pass


class BaseAgent(ABC):

	def __init__(self, deck, **child_attr):
		# use deque instead of list for easier hand manipulations
		random.shuffle(deck)
		self.deck = deque(deck)

		# create starting hand
		self.hand: list[BaseCard] = []
		self.make_hand()



		self.name = child_attr.get('name')
		self.hp = child_attr.get('hp', 5)
		self.max_hp = child_attr.get('max_hp', 5)
		self.shield = child_attr.get('shield', 0)  # lasting shield
		self.t_shield: list[list[int, int]] = child_attr.get('t_shield', [])  # shield that goes away after x rounds)
		self.ammo = child_attr.get('ammo', 0)
		self.attack = child_attr.get('attack', 1)
		# self.deck = child_attr['deck']
		self.effects = child_attr.get('effects', [])
		self.active_priority = child_attr.get('active_priority', 50)

		self.shield_total = None
		self.calc_shield()  # calculated number


		self.energy = 1

	def make_hand(self):
		self.hand = list(itertools.islice(self.deck, 3))


	def use_card(self, card_index, target, short_hand=None):
		selected_card: BaseCard = self.hand[card_index - 1]

		# we don't want to execute both cards at the same time, so lets return the card
		# and get the parent function to add it to the action queue.

		# remove card from hand, move it to last position in queue
		self.deck.popleft()
		self.deck.append(selected_card)

		self.make_hand()

		# some cards will have querys, others will not, provide all necessary info, each card's
		# query will grab and use info they need
		selected_card.query(
			caster=self,
			target=target,
			short_hand=short_hand,
		)


		return selected_card

	def log_cards(self):
		out = ""
		for i, card in enumerate(self.hand):
			out += f"[{i+1}] - {card.name}\n"

		out += f"next card: {self.deck[3].name} \n"  # also show next card in deck
		return out

	def calc_damage(self) -> int:
		return self.attack

	# @abstractmethod
	def take_damage(self, inc_damage: int, true_damage=False) -> (bool, int):
		# subtract off temporary shield, then lasting shields, then hp
		# assuming temp shields are sorted in order of breaking first to breaking last

		# [(1, 2), (2, 2), (1, 3)]
		# broken = [0 for _ in self.t_shield]

		if true_damage:
			if self.hp > inc_damage:
				self.hp -= inc_damage

			else:
				self.die()

			return True, inc_damage

		# if the damage is not true damage: run the following code.

		strength = inc_damage
		for i,(t_amt, t_dur) in enumerate(self.t_shield):
			if strength > t_amt:
				strength -= t_amt
				# broken[i] = 1
				self.t_shield[i][1] = 0 # set t_dur to 0
			else:
				self.t_shield[i][0] -= strength
				strength = 0
				break





		# lets go ahead and test for lasting shield

		if strength > self.shield:
			strength -= self.shield
			self.shield = 0
		else:
			self.shield -= strength
			strength = 0

		if strength == 0:
			return False, 0

		if self.hp > strength:
			self.hp -= strength

		else:
			self.die()

		return True, strength


	def add_ammo(self, ammo_amt):
		print("AMMO ADDED")
		self.ammo += ammo_amt


	def die(self):
		print(f"{self.name} has DIED!")
		self.hp = 0
		del self


	def heal(self, healing_amt: int):
		self.hp = min(self.max_hp, self.hp+healing_amt)


	def add_max_hp(self, max_hp_amt: int):
		# update ui
		self.max_hp += max_hp_amt
		self.hp += max_hp_amt # raw value update, not funneling through heal()


	def add_t_shield(self, shield_amount, duration):
		self.t_shield.append(	  [shield_amount, duration]		)
		self.calc_shield()
		# TODO: make sure shield manager calls calc_shield every time a shield is changed


	def add_shield(self, shield_amount):
		self.shield += shield_amount
		self.calc_shield()


	def calc_shield(self):
		self.shield_total = self.shield + sum(map(lambda x: x[0], self.t_shield))


	def add_effect(self, new_effect):
		self.effects.append(new_effect)


	def can_use_active(self):
		return True


	def possible_actions(self):
		return """
		c (n) - play card n
		a use - use active
		f - finish turn
		"""

	def query(self, target):
		# # player uses active?
		# use_active = False
		# if self.can_use_active():
		# 	try:
		# 		use_active = bool(int(input('active use? [0] to hold, [1] to use: ')))
		# 	except:
		# 		pass
		#
		# # player picks card
		# card_choice = None
		# while card_choice not in range(0, hand_size+1):
		# 	card_choice = int(input('card choice: '))
		#
		# return card_choice, use_active

		def generate_action_event(priority, execute, caster, target):
			action_event = {}
			for item in ['priority', 'execute', 'caster', 'target']:
				action_event[item] = locals()[item]

			return action_event

		new_action_events = []

		while True:
			print("[?] for list of commands")
			k, *raw_in = input("enter command: ").split(' ')

			if k == '?':
				print(self.possible_actions())
			elif k == 'c':

				params = list(map(int, raw_in))

				sh = None if len(params) == 1 else params[1]
				print(f"SHHHH is {sh}")

				selected_card = self.use_card(
					card_index=params[0], target=target,
					short_hand=sh
				)

				action_event = generate_action_event(
					priority=selected_card.priority,
					execute=selected_card.execute,
					caster=self,
					target=target,
				)

				new_action_events.append(action_event)
			elif k == 'a' and raw_in[0] == 'use':
				action_event = generate_action_event(
					priority=self.active_priority,
					execute=self.active,
					caster=self,
					target=target,
				)

				new_action_events.append(action_event)
			elif k == 'f':
				return new_action_events





	def on_round_start(self, target):
		self.passive(target)
		print()
		print(self.log_agent_info())
		print(self.log_cards())
		# self.effects()

	def on_round_end(self, target):
		# decay shields and effects

		# for shields

		to_be_removed = []

		for i, (strength, duration) in enumerate(self.t_shield):
			if duration == 0:
				to_be_removed.append(self.t_shield[i])
			else:
				self.t_shield[i][1] -= 1

		for t_shield in to_be_removed:
			self.t_shield.remove(t_shield)

		self.calc_shield()

		print(f"my shields\t\t\t\t\t {self.t_shield}")


	def log_agent_info(self):
		return f"{self.name}: {self.shield_total}🛡️ {self.hp}/{self.max_hp}❤ {self.ammo}ammo"

	@abstractmethod
	def passive(self, target):
		# called at the beginning of each round
		pass

	@abstractmethod
	def active(self, **child_args):
		# called when player activates active during choice phase...
		pass

	def on_attack_card(self, target):
		target.take_damage(self.calc_damage())
		self.add_ammo(-1)

	def on_ammo_card(self, target):
		self.add_ammo(1)

	def on_defend_card(self, target):
		self.add_t_shield(shield_amount=2, duration=1)

	def on_heal_card(self, target):
		self.heal(1)



# def effects(self):
	# 	# called at the beginning of each round
	# 	# manage the effects on the current player
	# 	pass

