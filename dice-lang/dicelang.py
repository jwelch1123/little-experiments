import re
import random

def roll(dice):
	pattern = re.compile(r"(avg +|count +)?(\d+)?(d\d+|D\d+)(a(?!m|l)|d(?!l|h))?(\+\d+|-\d+)?(kh\d+|kl\d+|dh\d+|dl\d+)?(am\d+|al\d+)?((?:rr\d+)+)?")

	roll_results = [] # list of tuples with (rolls, values)

	for match in pattern.finditer(dice):
		aggregation = match.group(1).lower()           if match.group(1) else '' 
		n_dice      = int(match.group(2))              if match.group(2) else 1
		dice_name   = match.group(3)                   if match.group(3) else None
		n_sides     = int(re.sub(r"\D","",dice_name))  if dice_name else None
		adv_dis     = match.group(4)                   if match.group(4) else ''
		modifier    = int(match.group(5))              if match.group(5) else 0 # add space detection
		drop_keep   = match.group(6)                   if match.group(6) else None
		drp_kp_rule = re.sub(r'\d','', drop_keep)      if drop_keep else ''
		drp_kp_val  = int(re.sub(r'\D','', drop_keep)) if drop_keep else None
		limit       = match.group(7)                   if match.group(7) else None
		lmt_rule    = re.sub(r'\d','', limit)          if limit else ''
		lmt_val     = int(re.sub(r'\D','', limit))     if limit else None
		reroll      = match.group(8)                   if match.group(8) else None
		reroll_vals = [int(x.group(0)) for x in re.compile(r"\d+").finditer(reroll)] if reroll else []
		
		print("Dice Expression: ", pattern.match(dice).group(0))
		#print(f"Rolling {n_dice} {dice_name} with {adv_dis} and {drop_keep} and {limit} with a modifier or {modifier} and rerolling {reroll_vals} and aggregating on {aggregation}")
	
		results = []
		for i in range(n_dice):
			
			# roll the dice
			match adv_dis.lower():
				case "a":
					ad_func = max
				case "d":
					ad_func = min
				case _:
					ad_func = lambda x, y: x
			
			# Rerolls
			reroll_func = lambda x: x if x not in reroll_vals else random.randint(1,n_sides)
			
			roll = ad_func(reroll_func(random.randint(1,n_sides)), reroll_func(random.randint(1,n_sides)))
			results.append(roll)
		
		# apply drop/keep rule
		match drp_kp_rule.lower():
			case "kh":
				kp_func = lambda x: sorted(x)[-drp_kp_val:]
			case "kl":
				kp_func = lambda x: sorted(x)[:drp_kp_val]
			case "dh":
				kp_func = lambda x: sorted(x)[:-drp_kp_val]
			case "dl":
				kp_func = lambda x: sorted(x)[drp_kp_val:]
			case _:
				kp_func = lambda x: x

		results = kp_func(results)

		# apply limit rule
		match lmt_rule.lower():
			case "am":
				lmt_func = lambda x: [x for x in x if x <= lmt_val]
			case "al":
				lmt_func = lambda x: [x for x in x if x >= lmt_val]
			case _:
				lmt_func = lambda x: x

		results = lmt_func(results)


		# Aggregate the results
		# currently this is running on the subsequent roll expression not across multiple
		match aggregation.lower().strip(): 
			case "avg":
				agg_func = lambda x, y: (sum(x) / len(x)) + y 
			case "count":
				agg_func = lambda x, y: len(x)
			case _:
				agg_func = lambda x, y: sum(x) + y
		
		total = agg_func(results, modifier)

		roll_results.append((results, total))

	roll_str = "".join([f"{x} for a result of {y}\n" for x, y in roll_results])

	print(f"You rolled \n {roll_str}")			

	pass

def main():
	# examples = [
	# 	"d2", "2d4","3d6d", "d100a", "d20-2", "avg 4d12+3",
	# 	"10d100dl9", "10d100dh9", "10d100kl9", "10d100kh9",
	# 	"10d100am9", "10d100al9", "10d2rr1", "2d4 10d20+4"]
	# for i in examples:
	# 	print("Rolling: ", i)
	# 	roll(i)
		
	print("Enter Roll or 'exit' to quit")
	while True:
		dice = input("Enter a dice roll expression: ")
		if dice == "exit":
			break
		elif dice == "quit":
			break
		elif dice == "":
			continue
		else:
			roll(dice)

if __name__ == "__main__":
	main()