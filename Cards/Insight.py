from Base import BaseAgent, BaseCard


class InsightCard(BaseCard):
	def __init__(self):
		super().__init__(
			name="Insight",
			energy_cost=1,
			priority=50,
		)

	def execute(self, caster: BaseAgent, target: BaseAgent):
		pass
		# TODO: to be implemented
