from Base import BaseAgent, BaseCard


class DefendCard(BaseCard):
	def __init__(self):
		super().__init__(
			name="Defend",
			energy_cost=1,
			priority=60
		)

	def execute(self, caster: BaseAgent, target: BaseAgent):
		caster.on_defend_card(target)
