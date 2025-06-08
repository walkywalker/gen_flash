class question_format_base(object):
	Q_AUDIO = True
	Q_TEXT = True
	Q_TEXT_LANG_IS_PRIMARY = True

	def __init__(self, primary, secondary):
		self.primary = primary
		self.secondary = secondary

	def get_question(self):
		if not self.Q_TEXT:
			return ""	
		elif self.Q_TEXT_LANG_IS_PRIMARY:
			return self.primary
		else:
			return self.secondary

	def get_answer(self):
		if self.Q_TEXT_LANG_IS_PRIMARY:
			return self.secondary
		else:
			return self.primary


class secondary_text_only(question_format_base):
	Q_AUDIO = False
	Q_TEXT = True
	Q_TEXT_LANG_IS_PRIMARY = False


class secondary(question_format_base):
	Q_AUDIO = True
	Q_TEXT = True
	Q_TEXT_LANG_IS_PRIMARY = False


class secondary_audio_only(question_format_base):
	Q_AUDIO = True
	Q_TEXT = False
	Q_TEXT_LANG_IS_PRIMARY = False


class primary(question_format_base):
	Q_AUDIO = False
	Q_TEXT = True
	Q_TEXT_LANG_IS_PRIMARY = True
	