import os, pygame, json, random, csv, math, threading, sys
from pygame.locals import *
from utils import *
from dalesutils import *

COMBO_BTNS = {K_a:"A", K_s:"S", K_d:"D", K_f:"F", K_SPACE:"SPACE"}

class ComboState():
	def __init__(self, (main_sheet, dims), spritesheets):
		''' main_sheet should be a filename for the default sprite sheet
			spritesheets should give a list of spritesheet image tuples
			("name", "filename.jpg", (dims)) ex. None should be duplicate names.
			dims should be an (x, y, k) tuple which gives the width, height
			and number of sprite images in the sprite sheet. '''
		self.sheet_map = []
		for (name, filename, dims_l) in spritesheets:
			image, img_rect = load_image_alpha(filename)
			self.sheet_map.append((name,(image, img_rect), extract_frames_from_spritesheet(img_rect, dims_l[0], dims_l[1], dims_l[2])))
		self.cur_sheet, self.cur_rect = load_image_alpha(main_sheet)	
		self.cur_frames = extract_frames_from_spritesheet(self.cur_rect, dims[0], dims[1], dims[2])
		self.def_frames = self.cur_frames
		self.def_sheet = self.cur_sheet
		self.def_rect = self.cur_rect
		self.frame_index = 0
		self.repeat_frames, self.repeated = 8, 0	#repeat the last frame of a combo /repeat_frames/ times
		self.combo_no = 0
		self._advance_key = K_SPACE #what key to press to advance
		self.can_advance = True
		
	def enter_state(self, sheetname):
		''' enter a state by its name '''
		((self.cur_sheet, self.cur_rect), self.cur_frames) = self.find_state(sheetname)
	
	def interrupt(self):
		''' Break out of the combo state to the default sheet '''
		self._advance_key = K_SPACE #reset combo starting key to space
		self.can_advance = True
		if self.cur_sheet is not self.def_sheet:
			self.cur_sheet = self.def_sheet
			self.cur_frames = self.def_frames
			self.cur_rect = self.def_rect
			self.combo_no = 0
			self.frame_index = 0
		return (self.cur_sheet, self.cur_rect), self.cur_frames
	
	def enter_combo(self):
		''' Enter the combo state '''
		self.combo_no = 0
		return self.advance()
	
	def advance(self, override = False):
		''' Advance the combo by one state '''
		#print 'Pressed Combo Button'
		if self.sheet_map:
			if override or self.can_advance:
				self.combo_no += 1
				self.combo_no %= len(self.sheet_map)
				self.frame_index = 0
				self.cur_sheet, self.cur_rect = self.sheet_map[self.combo_no-1][1]
				self.cur_frames = self.sheet_map[self.combo_no-1][2]
			else:
				return None
		return self.get_cur_frame()
	
	def find_state(self, sheetname):
		''' find a state by its name '''
		for (name, attrs, frames) in self.spritesheets:
			if name is sheetname: return (attrs, frames)
			
	def get_cur_state(self):
		return self.cur_sheet
	
	def get_cur_frame(self):
		#self.constrain_frame_index()
		self.cur_image = self.cur_sheet.subsurface( self.cur_frames[self.frame_index] )
		return self.cur_image
		
	def get_cur_frame_and_progress(self):
		if self.cur_sheet is not self.def_sheet:
			self.combo_check()
		else:
			self.frame_index %= len( self.cur_frames ) #default sheet, repeat
		self.cur_image = self.cur_sheet.subsurface( self.cur_frames[self.frame_index] )
		self.frame_index += 1
		return self.cur_image
		#return self.cur_sheet[old_frame]
	
	def combo_check(self):
		''' give the player some frame queues to advance the combo,
			but end it if he has exceeded the max queue frames'''
		if self.frame_index >= len( self.cur_frames ):
			if self.repeated == 0:
				self.select_combo_key()	#randomly select key for combo advance
			self.display_combo_key()
			self.can_advance = True
			if self.repeated >= self.repeat_frames:
				self.interrupt()
				return
			self.frame_index = len( self.cur_frames ) - 1
			self.repeated +=1
		else:
			self.can_advance = False
			self.repeated = 0
	
	def get_combo_key(self):
		return self._advance_key
			
	def check_combo_key(self):
		pressed = pygame.key.get_pressed()
		if( len( list(set(pressed).intersection(list(COMBO_BTNS.keys())) )) > 1):
			return False
		'''print "Needed to press: ", COMBO_BTNS[self._advance_key]
		print "Key was pressed?: ", pressed[self._advance_key]'''
		return pressed[self._advance_key]

	def select_combo_key(self):
		self._advance_key  = random.choice(list(COMBO_BTNS.keys()))
	
	def display_combo_key(self):
		keytext = COMBO_BTNS[self._advance_key]
		disp = pygame.display.get_surface()
		x_coord = disp.get_width()/2 - 10 * len(keytext)
		display_text(disp, keytext, x_coord, 10, size=35)	
