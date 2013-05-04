MERWAR
Tanya Presnetsova, Dale Gartman, Randall Hanak

To run MERWAR:
python merwarmain.py

Controls:
	The ARROW keys control movement.
	SHIFT dodges (has a cooldown, not yet displayed).
		Pay attention to know when to dodge. Enemies will display a pullback
		animation and sound. Dodge when they are poised to strike.
	COMBO MOVES:
		CTRL->CTRL->CTRL Simple attack
		CTRL->ALT->CTRL Double Smash attack
		CTRL->SPACE->CTRL Dervish attack

Gameplay:	
	Combo Moves can be chained together, and each attack has a 50% chance of interrupting
	each enemy it hits. Be careful though - If they hit you, it WILL interrupt your combo.
	
	To fight, swim within range of enemies and use the Combo Moves. 
	
	To chain together a Combo, watch for the brief pause in animation at the end of a move.
	Try to complete the combo key sequence during this pause. 
	
	You can also chain dodging into combos.

	Difficulty:
		To move to a more challenging difficulty level, swim downward to the screen edge.
		To move to an easier level, swim upward.
		
		The timers will keep track of how long you are on each level!
	
	To advance to the next page, swim to the right.
	
Code Structure:
	GameEngine - abstracts the game loop, holds page data.
	Mermaid - Holds protagonist code
	CharManager - handles character update actions and interactions between the characters
	Characters - holds antagonist code
	dalesutils - simple text display functions
	Item - Health starfish sprite
	merwarmain - game loop. Does some other magic and calls GameEngine.
	ComboState - State machine for combos and animation, used by CharManager
	AbstractChar - notification/event system superclass for Characters
	
