from Base import BaseAgent


class Colossus(BaseAgent):
	def __init__(self, deck):
		super().__init__(deck,
			name='Colossus',
			hp=6,
			max_hp=6,
			shield=0,
			ammo=0,
			attack=1,
			active_priority=60,
		)
		self.rage = 0
		self.enraged = False # add the extra damage point
		self.attack_bonus = 0

	def deal_damage(self) -> int:
		return self.attack + self.attack_bonus

	def take_damage(self, inc_damage: int, true_damage=False) -> (bool, int):
		successful, hp_lost = super().take_damage(inc_damage, true_damage)
		self.add_rage(hp_lost)
		return successful, hp_lost

	def add_rage(self, rage_amt):
		self.rage = min(5, self.rage + rage_amt)
		print(f"COLOSSUS: Rage Building...")


	def passive(self, target):
		if self.rage >= 3:
			self.enraged = True
			self.attack_bonus = 1
			print("COLOSSUS: NOW I'M ANGRY")
		else:
			self.enraged = False
			self.attack_bonus = 0


	def can_use_active(self):
		if self.rage >= 5:
			return True

		return False

	def active(self, **child_args):
		self.rage = 0
		self.max_hp += 3
		self.heal(healing_amt=3)


	def log_agent_info(self):
		return super().log_agent_info() + f" {self.rage}/5 rage"
