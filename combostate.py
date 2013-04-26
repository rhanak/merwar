import os, pygame, json, random, csv, math
from pygame.locals import *
from utils import *

class ComboState():
	def __init__(self, main_fname, spritesheets, dims):
		''' main_sheet should be a filename for the default sprite sheet
			spritesheets should give a list of spritesheet image tuples
			("name", "filename.jpg") ex. None should be duplicate names.
			dims should be an (x, y, k) tuple which gives the width, height
			and number of sprite images in the sprite sheet. '''
		print "Dims: ", dims
		self.sheet_map = []
		for (name, filename) in spritesheets:
			image, img_rect = load_image_alpha(filename)
			self.sheet_map.append((name,(image, img_rect), extract_frames_from_spritesheet(img_rect, dims[0], dims[1], dims[2])))
		self.cur_sheet, self.cur_rect = load_image_alpha(main_fname)	
		self.cur_frames = extract_frames_from_spritesheet(self.cur_rect, dims[0], dims[1], dims[2])
		self.def_frames = self.cur_frames
		self.def_sheet = self.cur_sheet
		self.def_rect = self.cur_rect
		self.frame_index = 0
		self.combo_no = 0
		
	def enter_state(self, sheetname):
		''' enter a state by its name '''
		((self.cur_sheet, self.cur_rect), self.cur_frames) = self.find_state(sheetname)
	
	def interrupt(self):
		''' Break out of the combo state to the default sheet '''
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
	
	def advance(self):
		''' Advance the combo by one state '''
		print 'Pressed Combo Button'
		
		if self.sheet_map:
			self.combo_no += 1
			self.combo_no %= len(self.sheet_map)
			self.frame_index = 0
			self.cur_sheet, self.cur_rect = self.sheet_map[self.combo_no-1][1]
			self.cur_frames = self.sheet_map[self.combo_no-1][2]
		return self.get_cur_frame()
	
	def find_state(self, sheetname):
		''' find a state by its name '''
		for (name, attrs, frames) in self.spritesheets:
			if name is sheetname: return (attrs, frames)
			
	def get_cur_state(self):
		return self.cur_sheet
	
	def get_cur_frame(self):
		self.cur_image = self.cur_sheet.subsurface( self.cur_frames[self.frame_index] )
		return self.cur_image
		
	def get_cur_frame_and_advance(self):
		old_ind = self.frame_index
		self.frame_index += 1
		self.frame_index %= len( self.cur_frames )
		self.cur_image = self.cur_sheet.subsurface( self.cur_frames[old_ind] )
		return self.cur_image
		#return self.cur_sheet[old_frame]
		
