class GameLogger:
	def log(self, event):
		"""
		Parameters:
			event (One of `events.EVENT_CLASSES`): An event that changed the game state.
		"""
		raise NotImplementedError()
