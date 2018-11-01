class Action:
	def __init__(self, tag, text = None, children = [], attributes={}):
		self.tag = tag
		self.xml = ""
		self.text = text
		self.children = children
		self.attributes = attributes
	def build(self):
		self.xml = "<" + self.tag
		if bool(self.attributes):
			for key in self.attributes:
				self.xml += " " + key + "=" + self.attributes[key] + " "
		self.xml += ">"

		if self.text is not None:
			self.xml += self.text
		if len(self.children) > 0:
			for child in self.children:
				self.xml += child.build()
		self.xml += "</" + self.tag + ">"
		return self.xml
