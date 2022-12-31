# implement single player as of now

# (choice) 	player 1 & 2 pick their cards
# (playing)	cards played simultaneously
#

import enum





from Base import BaseAgent
from Cards.Attack import AttackCard
from Cards.Defend import DefendCard
from Characters.Colossus import Colossus
from Characters.Cultist import Cultist


class State(enum.Enum):
	choice = 0
	reveal = 1







class Game:
	def __init__(self, agent1: BaseAgent, agent2: BaseAgent):
		self.agent1 = agent1
		self.agent2 = agent2

		self.action_queue = [] # filled with action events

	def choice_phase(self):
		# 1. show players their cards
		# query each player on what they want to do:
		#  2a. activate any active abilities
		#  2b. use any cards

		def per_player_actions(my: BaseAgent, your: BaseAgent):

			# print user's stats
			my.on_round_start(your)

			self.action_queue.extend(my.query(your))



		per_player_actions(self.agent1, self.agent2)
		per_player_actions(self.agent2, self.agent1)

	def reveal_phase(self):
		# selected_card.execute(self.agent, your.agent)

		# sort action q first
		# HIGHER PRIORITY values played FIRST
		print(self.action_queue)
		self.action_queue.sort(key=lambda action_event: action_event['priority'], reverse=True)

		# then run
		for priority, action, caster, target in map(dict.values, self.action_queue):
			action(caster=caster, target=target)

		self.action_queue.clear()

		# decay shields and effects



		self.agent1.on_round_end(self.agent2)
		self.agent2.on_round_end(self.agent1)




state = State.choice

henry_deck = [AttackCard() for _ in range(7)] + [DefendCard() for _ in range(2)]
vlad_deck = [AttackCard() for _ in range(5)] + [DefendCard() for _ in range(4)]

henry = Cultist(henry_deck)
vlad = Colossus(vlad_deck)




game = Game(henry, vlad)

turn = 1
running = True
while running:


	# take input from player 1 and 2
	print("-"*40 + f"TURN {turn}" + "-"*40)
	game.choice_phase()
	game.reveal_phase()
	turn += 1



