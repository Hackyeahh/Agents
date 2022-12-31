from Base import BaseAgent, BaseCard


class AttackCard(BaseCard):
	def __init__(self):
		super().__init__(
			name="Attack/Ammo",
			energy_cost=1,
			priority=40
		)

		self.use_as_attack_card = None


	def query(self, caster=None, short_hand=None, **other_args):
		if not caster:
			raise "Hook up the query with a caster parameter."


		can_use_attack = self.can_execute(caster)
		if not can_use_attack:
			print("created 1 ammo")
			self.use_as_attack_card = False
			return

		if short_hand is not None:
			self.use_as_attack_card = not bool(short_hand)
			return

		print("[0] - Attack")
		print("[1] - Ammo")

		choice = None
		while choice not in (0,1):
			choice = int(input("your choice --> "))


		self.use_as_attack_card = not bool(choice)

	def can_execute(self, caster):
		# signifies if the attack card can be played
		if caster.ammo == 0:
			return False

		return True

	def execute(self, caster: BaseAgent, target: BaseAgent):
		if self.use_as_attack_card:
			caster.on_attack_card(target)
		else:
			caster.on_ammo_card(target)
