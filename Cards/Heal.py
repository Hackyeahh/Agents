from Base import BaseAgent, BaseCard


class HealCard(BaseCard):
	def __init__(self):
		super().__init__(
			name="Heal",
			energy_cost=1,
			priority=60,
		)

	def execute(self, caster: BaseAgent, target: BaseAgent):
		caster.on_heal_card(target)