#coded by Tanya Presnetsova, Assignment 2, due 2/13/13 @10pm

import os, pygame, json, random, csv
from pygame.locals import *
if not pygame.mixer: print 'Warning: sound disabled'
from utils import *
from modes import ModeManager, GameMode, SimpleMode
from characters import *

kDataDir = 'data'
kGlobals = 'globals.json'
    
def main():
  pygame.init()
  screen = pygame.display.set_mode((900,630))
  pygame.display.set_caption('Shark Tag')
  pygame.mouse.set_visible(0)
  
  unselected = 1
  splashScreen = pygame.image.load(path_rejoin('data/select_screen.png')).convert()
  quit_rect = pygame.Rect( 25, 100, 140, 160 )
  start_rect = pygame.Rect( 25, 25, 145, 90 )
  mouse_down_pos = (-1,-1)
  pygame.mouse.set_visible( 1 )
  
  while unselected:
    for event in pygame.event.get():
      if event.type == MOUSEBUTTONDOWN:
        mouse_down_pos = event.pos
      elif event.type is MOUSEBUTTONUP:
        def collides_down_and_up( r ):
          return r.collidepoint( mouse_down_pos ) and r.collidepoint( event.pos )
        if collides_down_and_up( quit_rect ):
          print 'quitting'
          return   
        if collides_down_and_up( start_rect ):
          print 'play!'
          unselected = 0
          break
    screen.blit(splashScreen, (0,0))
    pygame.display.flip()
  
  
  '''background = pygame.image.load(path_rejoin('data/underthesea.png')).convert()'''
  backgroundEasy = pygame.image.load(path_rejoin('data/undertheseaeasy.png')).convert()
  backgroundNormal = pygame.image.load(path_rejoin('data/underthesea.png')).convert()
  backgroundHard = pygame.image.load(path_rejoin('data/undertheseahard.png')).convert()
  screen.blit(backgroundNormal,(0,0))
  pygame.display.flip()
  
  clock = pygame.time.Clock()
  whiff_sound = load_sound('bubbles.wav')
  stab_sound = load_sound('bubbleshit.wav')
  sharkManager = SharkManager()
  sharkgroup = pygame.sprite.Group( sharkManager.returnSharks() )
  for character in csv.DictReader( open( os.path.join( kDataDir, 'maze_characters.csv' ) ) ):
    mermaid = Mermaid(character, sharkgroup, sharkManager)
  mermaidg = pygame.sprite.Group( ( mermaid ) )
  
  while 1:
    clock.tick(15)
    pygame.mouse.set_visible( 0 )
    
    for event in pygame.event.get():
      if event.type == QUIT:
        return
      elif event.type == KEYDOWN and event.key == K_ESCAPE:
        return
      elif event.type == MOUSEBUTTONDOWN:
        killed = pygame.sprite.spritecollide(mermaid, sharkgroup, True )
        if len( killed ) > 0:
          stab_sound.play()
        else:
          whiff_sound.play()
      elif event.type is MOUSEBUTTONUP:
        mermaid.unstab()
        
    changeInDifficulty=mermaid.update()
    if (changeInDifficulty):
      sharkgroup.empty()
      sharkgroup = pygame.sprite.Group( sharkManager.returnSharks() )
    sharkgroup.update()
    
    if(difficulty=="easy"):
      screen.blit(backgroundEasy, (0,0))
    elif(difficulty=="normal"):
      screen.blit(backgroundNormal, (0,0))
    elif(difficulty=="hard"):
      screen.blit(backgroundHard, (0,0))
    sharkgroup.draw(screen)
    mermaidg.draw(screen)
    pygame.display.flip()
    
if __name__== '__main__': main()
      















