import re
import random

# rule set
# https://tableplop.notion.site/Dice-rolling-syntax-options-37ef6202bdc44e288b7eb84dc344dabc
# https://docs.python.org/3/library/re.html

# d# = roll a # sided die
# d#a or d is advantage/disadvantage
# rr# = reroll #s
# kh# = keep highest #s
# kl# = keep lowest #s
# dh# = drop highest #s
# dl# = drop lowest #s
# am# = at most
# at# = at least
# count ex
# avg ex 


available_dice = ["d2","d4", "d6", "d8", "d10", "d12", "d20", "d100"]

def roll(dice):
	pattern = re.compile(r"(\d+)?(d\d+)(a|d)?")

	#print(pattern.search(dice))
	# print the capture groups
	#print(pattern.search(dice).groups())

	for match in pattern.finditer(dice):
		n_dice  = match.group(1) if match.group(1) else 1
		dice_name = match.group(2)
		n_sides = int(dice_name.replace("d", ""))
		adv_dis = match.group(3)

		print(f"rolling a {dice_name} {n_dice} times with {adv_dis}")
	
		for i in range(n_dice):
			roll = random.randint(1	,n_sides)
			



	pass

def main():
	roll("d2")
	roll("2d4")
	roll("3d6d")
	roll("4d8a")

if __name__ == "__main__":
	main()