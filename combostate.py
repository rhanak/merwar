import pygame, random, math
from pygame.locals import *
from utils import *
from dalesutils import *

DODGE_COOLDOWN = 1250

class ComboMachine():
	def __init__(self, main_state, spritesheets, dodging_state=None):
		''' main_state and dodging_state are tuples (filename, (dims))
			spritesheets should give a list of spritesheet image tuples
			("keysequence", "filename.jpg", (dims)) ex. None should be duplicate names.
			dims should be an (x, y, k) tuple which gives the width, height
			and number of sprite images in the sprite sheet.
			'''
		main_sheet, dims = main_state
		self.state_map = {}
		self.MAX_COMBO_LEN = 0
		for (keysequence, filename, dims_l) in spritesheets:
			image, img_rect = load_image_alpha(filename)
			self.MAX_COMBO_LEN = max(self.MAX_COMBO_LEN, len(keysequence))
			#print img_rect
			state = ComboState((image, img_rect), extract_frames_from_spritesheet(img_rect, dims_l[0]-1, dims_l[1]-1, dims_l[2]))
			state.set_circular(False)
			self.state_map[keysequence] = state
		
		def_sheet, def_rect = load_image_alpha(main_sheet)	
		def_frames = extract_frames_from_spritesheet(def_rect, dims[0], dims[1]-1, dims[2])
		self.cur_state = ComboState( (def_sheet, def_rect), def_frames) 
		self.state_map["DEFAULT"] = self.cur_state
		if dodging_state: 
			dodge_name, dodge_dims = dodging_state
			dodge_image, dodge_rect = load_image_alpha(dodge_name)
			dodge_state = ComboState( (dodge_image, dodge_rect),\
				extract_frames_from_spritesheet(dodge_rect, dodge_dims[0]-1, dodge_dims[1]-1, dodge_dims[2]))
			dodge_state.set_circular(False)
			self.state_map["DODGING"]  = dodge_state
		self.repeat_frames, self.repeated = 10, 0	#repeat the last frame of a combo /repeat_frames/ times
		self.combo_no = 0
		#self._advance_key = K_SPACE #what key to press to advance
		self.combo_sequence = ""
		self.can_advance = True
		self.dodge_timer = pygame.time.Clock()
		self.dodge_cd = DODGE_COOLDOWN
	
	def interrupt(self, bypass_dodging=False):
		''' Break out of the combo state to the default sheet '''
		#self._advance_key = K_SPACE #reset combo starting key to space
		self.can_advance = True
		dodge_var = bypass_dodging or not self.dodging()
		if not self.in_default_state() and dodge_var:
			#print "Combo chain: ", self.combo_no
			if self.dodging(): self.dodge_cd = 0
			self.cur_state = self.state_map["DEFAULT"]
			self.combo_no = 0
			self.repeated = 0
			self.combo_sequence = ""
	
	def in_default_state(self):
		return self.cur_state is self.state_map["DEFAULT"]
		
	def dodging(self):
		if self.state_map.has_key("DODGING"):
			return self.cur_state is self.state_map["DODGING"]
		return False
			
	def get_num_frames(self):
		return len(self.cur_state.frames)
	
	def find_state(self, sheetname):
		''' find a state by its name '''
		if self.state_map.has_key(sheetname):
			return self.state_map[sheetname]
		return None
	
	def get_cur_frame(self, opt_index=-1):
		if opt_index>=0:
			self.cur_state.index = opt_index	
		return self.cur_state.get_frame()	
		
	def get_cur_frame_and_progress(self):
		return self.cur_state.get_frame_and_progress()
		#return self.cur_image
		#return self.cur_sheet[old_frame]
		
	def try_dodge(self):
		if self.dodging() or self.dodge_cd < DODGE_COOLDOWN:
			return
		else:
			self.begin_dodge()
	
	def begin_dodge(self):
		if self.state_map.has_key("DODGING"):
			self.enter_combo_str("DODGING")
		
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
	
	def enter_combo_str(self, str):
		state = self.find_state(str)
		self.enter_combo_state(state)
	
	def enter_combo_state(self, state):
		''' enter a state '''
		state.reset()
		if(state == self.cur_state):
			state.reduce_multiplier()
		else:
			state.reset_multiplier()
		self.combo_sequence = ""
		self.repeated = 0
		self.cur_state = state
		self.combo_no += 1
		self.can_advance = False
		
	def get_damage_multiplier(self):
		return self.cur_state.diminish_multiplier
	
	def combo_check_and_update(self, keysequence = ""):
		''' give the player some frame queues to advance the combo,
			but end it if he has exceeded the max queue frames'''
		if(self.state_map.has_key("DODGING")):self.display_combo()
		self.combo_sequence+=keysequence
		#print "Current Combo: ", self.combo_sequence
		deft = self.in_default_state()
		if not self.dodging(): self.update_dodge_cd()
		else: self.dodge_timer.tick()
		if deft or not self.cur_state.did_advance():
			if deft: self.repeated = 0
			#if not self.cur_state.did_advance(): print "Didn't advance: ", self.repeated
			#print "repeated: ", self.repeated
			self.can_advance = True
			
			if self.repeated >= self.repeat_frames or (len(self.combo_sequence)>=self.MAX_COMBO_LEN):
				if not self.try_advance_combo():
					self.interrupt(True)
				return self.get_cur_frame_and_progress()
			#self.frame_index = len( self.cur_frames ) - 1
			if not deft: self.repeated +=1
		else:
			self.can_advance = False
			self.repeated = 0
		return self.get_cur_frame_and_progress()
		
	def display_combo(self):
		screen = pygame.display.get_surface()
		wid = screen.get_width()
		display_rage_text(screen, "Combo: " + str(self.combo_no), wid - 250, 10, 30)
		display_rage_text(screen, "Dmg Multiplier: "\
			 + "{0:.2f}".format(self.get_dmg_multiplier()), wid - 250, 60, 30)
	
	def update_dodge_cd(self):
		if self.dodge_cd <= DODGE_COOLDOWN:
			self.dodge_cd += self.dodge_timer.tick()
			#print "DODGE COOLDOWN REMAINING: ", DODGE_COOLDOWN- self.dodge_cd
			
	def get_dmg_multiplier(self):
		return self.cur_state.diminish_multiplier

class ComboState():
		def __init__(self, image_attrs, frames, circular = True):
			self.image, self.image_rect = image_attrs
			self.frames = frames
			#print frames
			self.index = 0
			self.circular = circular
			self.until_diminish = 0
			self.diminish_multiplier = 1.0
			self.advanced = True
			
		def reduce_multiplier(self):
			if (self.until_diminish > 0):
				self.until_diminish-=1
				return True
			else:
				dim_m = self.diminish_multiplier - .125
				self.diminish_multiplier = 0.0 if (dim_m <= 0) else dim_m
			return (self.diminish_multiplier > 0)
			
		def reset_multiplier(self):
			self.until_diminish = 0
			self.diminish_multiplier = 1.0
		
		def set_circular(self, circular = True):
			self.circular = circular
			
		def get_frame(self, index=-1):
			if index<0: 
				index = self.index
			elif index >= len(self.frames):
				if self.circular:
					index %= len(self.frames)
				else:
					index = len(self.frames)-1
			self.index = index
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
			
			