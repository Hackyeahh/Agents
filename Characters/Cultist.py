from Base import BaseAgent


class Cultist(BaseAgent):
	def __init__(self, deck):
		super().__init__(deck,
			name='Cultist',
			hp=3,
			max_hp=3,
			shield=0,
			ammo=1,  # starts with one ammo so it bypasses the check in Attack's can_execute()
			attack=1,
			active_priority=60,
		)
		self.dark_energy = 0
		self.turns_before_detonation = 4
		self.used_active = False



	def take_damage(self, inc_damage: int, true_damage=False) -> (bool, int):
		successful, hp_lost = super().take_damage(inc_damage, true_damage)
		self.add_dark_energy(hp_lost)
		return successful, hp_lost

	def add_dark_energy(self, dark_energy_amt):
		self.dark_energy += dark_energy_amt
		print(f"CULTIST: Collecting Energy" +  '%+d' % dark_energy_amt)


	def on_round_end(self, target: BaseAgent):
		super().on_round_end(target)
		self.turns_before_detonation -= 1


	def passive(self, target):
		if self.turns_before_detonation <= 0:
			target.take_damage(inc_damage=self.dark_energy)
			self.dark_energy = 0
			self.turns_before_detonation = 4


	def can_use_active(self):
		if self.dark_energy > 0 and not self.used_active:
			return True

		return False

	def active(self, **child_args):
		self.add_t_shield(self.dark_energy, 3)
		self.used_active = True


	def log_agent_info(self):
		return f"{self.name}: {self.shield_total}🛡️ {self.hp}/{self.max_hp}❤ " + \
			   f"{self.dark_energy}DE {self.turns_before_detonation}before DOOM"


	def on_attack_card(self, target):
		self.add_dark_energy(2)
		self.turns_before_detonation = 4

	def on_ammo_card(self, target):
		self.turns_before_detonation -= 1


