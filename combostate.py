def ComboState():
	def __init__(self, main_sheet, spritesheets, dims, ):
		''' main_sheet should be a filename for the default sprite sheet
			spritesheets should give a list of spritesheet image tuples
			("name", "filename.jpg") ex. None should be duplicate names.
			dims should be an (x, y, k) tuple which gives the width, height,
			and number of sprite images in the sprite sheet. '''
		self.sheets = spritesheets
		self.cur_sheet = main_sheet
		self.def_sheet = main_sheet
		self.combo_no = 0
		
	def enter_state(self, sheetname):
		self.cur_sheet = self.find_state(sheetname)
	
	def interrupt(self):
		self.cur_sheet = self.def_sheet
		self.combo_no = 0
		return self.cur_sheet
	
	def enter_combo(self):
		self.combo_no = 0
		return self.advance()
	
	def advance(self):
		self.combo_no += 1
		self.cur_sheet = self.spritesheets[self.combo_no-1][1]
		return self.cur_sheet
	
	def find_state(self, sheetname):
		for (name, filename) in self.spritesheets:
			if name is sheetname: return filename
		