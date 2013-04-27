import pygame, random, math
from pygame.locals import *
from utils import *
from dalesutils import *



class ComboMachine():
	def __init__(self, (main_sheet, dims), spritesheets):
		''' main_sheet should be a filename for the default sprite sheet
			spritesheets should give a list of spritesheet image tuples
			("keysequence", "filename.jpg", (dims)) ex. None should be duplicate names.
			dims should be an (x, y, k) tuple which gives the width, height
			and number of sprite images in the sprite sheet. '''
		self.state_map = {}
		self.MAX_COMBO_LEN = 0
		for (keysequence, filename, dims_l) in spritesheets:
			image, img_rect = load_image_alpha(filename)
			self.MAX_COMBO_LEN = max(self.MAX_COMBO_LEN, len(keysequence))
			print img_rect
			state = ComboState((image, img_rect), extract_frames_from_spritesheet(img_rect, dims_l[0], dims_l[1], dims_l[2]))
			state.set_circular(False)
			self.state_map[keysequence] = state
		
		def_sheet, def_rect = load_image_alpha(main_sheet)	
		def_frames = extract_frames_from_spritesheet(def_rect, dims[0], dims[1], dims[2])
		self.cur_state = ComboState( (def_sheet, def_rect), def_frames) 
		self.state_map["DEFAULT"] = self.cur_state
		self.repeat_frames, self.repeated = 10, 0	#repeat the last frame of a combo /repeat_frames/ times
		self.combo_no = 0
		#self._advance_key = K_SPACE #what key to press to advance
		self.combo_sequence = ""
		self.can_advance = True
	
	def interrupt(self):
		''' Break out of the combo state to the default sheet '''
		#self._advance_key = K_SPACE #reset combo starting key to space
		self.can_advance = True
		if not self.in_default_state():
			print "Combo chain: ", self.combo_no
			self.cur_state = self.state_map["DEFAULT"]
			self.combo_no = 0
			self.repeated = 0
			self.combo_sequence = ""
	
	def in_default_state(self):
		return self.cur_state is self.state_map["DEFAULT"]
	
	def enter_combo(self):
		''' Enter the combo state '''
		self.combo_no = 0
		return self.advance()
	
	def find_state(self, sheetname):
		''' find a state by its name '''
		if self.state_map.has_key(sheetname):
			return self.state_map[sheetname]
		return None
	
	def get_cur_frame(self):
		return self.cur_state.get_frame()
		
	def get_cur_frame_and_progress(self):
		return self.cur_state.get_frame_and_progress()
		#return self.cur_image
		#return self.cur_sheet[old_frame]
		
	def try_advance_combo(self):
		new_state = None
		keypresses = list(self.combo_sequence)
		frame_size = self.MAX_COMBO_LEN
		frame_start = 0
		#print "input: ", self.combo_sequence
		while frame_size > 0:
			while frame_start < (len(keypresses)):	
				real_size = min(len(keypresses)-frame_start, frame_size)
				if real_size <= 0: break
				query = ''.join(keypresses[frame_start:frame_start+real_size])
				#print "QUERY: ", query
				new_state = self.find_state(query)
				
				if new_state:
					print "COMBO FOUND: ", query
					self.enter_combo_state(new_state)
					return new_state
				frame_start += 1
			frame_size -= 1
		return new_state
	
	def enter_combo_state(self, state):
		''' enter a state '''
		state.reset()
		self.combo_sequence = ""
		self.repeated = 0
		self.cur_state = state
		self.combo_no += 1
		self.can_advance = False
	
	def combo_check_and_update(self, keysequence = ""):
		''' give the player some frame queues to advance the combo,
			but end it if he has exceeded the max queue frames'''
		self.combo_sequence+=keysequence
		#print "Current Combo: ", self.combo_sequence
		deft = self.in_default_state()
		if deft or not self.cur_state.did_advance():
			if deft: self.repeated = 0
			#if not self.cur_state.did_advance(): print "Didn't advance: ", self.repeated
			#print "repeated: ", self.repeated
			self.can_advance = True
			if self.repeated >= self.repeat_frames or (len(self.combo_sequence)>=self.MAX_COMBO_LEN):
				if not self.try_advance_combo():
					self.interrupt()
				return self.get_cur_frame_and_progress()
			#self.frame_index = len( self.cur_frames ) - 1
			if not deft: self.repeated +=1
		else:
			self.can_advance = False
			self.repeated = 0
		return self.get_cur_frame_and_progress()
	'''
	def get_combo_key(self):
		return self._advance_key'''
			
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

class ComboState():
		def __init__(self, image_attrs, frames, circular = True):
			self.image, self.image_rect = image_attrs
			self.frames = frames
			print frames
			self.index = 0
			self.circular = circular
			self.advanced = True
			
		def set_circular(self, circular = True):
			self.circular = circular
		
		def get_frame(self, index=None):
			if not index: 
				index = self.index
			return self.image.subsurface( self.frames[index] )
			
		def get_frame_and_progress(self):
			self.advance(self.circular)
			frame = self.get_frame(self.index)
			return frame
		
		def did_advance(self):
			if self.advanced:
				self.advanced = False
				return True
			else:
				return False
			
		def advance(self, circular = True):
			new_index = self.index + 1
			if circular:
				new_index %= len(self.frames)
			elif new_index >= len(self.frames):
				self.advanced = False
				return False		# repeat the frame
			self.index = new_index 
			self.advanced = True
			return True			# successfully advanced the frame
			
		def reset(self):
			self.index = 0
			
			