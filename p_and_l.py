# Generates a profit and loss curve given a list of option positions
# Mark Kraay - Aug 10, 2022

from collections import deque
import plotly.graph_objects as go
import pandas as pd

ENDPOINT_EXTENSION = 20

prompt = """
Positions should be entered in the form: position,amount,price,option,premium. For example: short,2,90,call,9.35 
(short two 90 calls at 9.35)
'Q' to stop reading positions
"""

options = []
print(prompt)
while True:
	try:
		inp = str(input("Enter a position: "))
		if inp.lower() == "q":
			break
		else:
			[position, amount, price, option, premium] = inp.split(",")
			options.append({"position": position, "amount": int(amount), "option": option, "price": float(price), "premium": float(premium)})
	except: 
		print(prompt)

print("Options entered.")
for option in options:
	print(option)

def process_options(options):
	assert len(options) > 0
	x = [] # Price
	y = [] # Profit

	num_calls = 0
	num_puts = 0
	for exercise_price in list(map(lambda option: option["price"], options)):
		profit = 0
		for option in options:
			price = option["price"]
			prem = option["premium"]
			amt = option["amount"]
			if option["option"] == "call":
				if option["position"] == "long":
					num_calls += amt
					gain = max(exercise_price - price - prem, -prem)
					profit += gain * amt
				elif option["position"] == "short":
					num_calls -= amt 
					gain = min(price - exercise_price + prem, prem)
					profit += gain * amt
			elif option["option"] == "put":
				if option["position"] == "long":
					num_puts += amt 
					gain = max(price - exercise_price - prem, -prem)
					profit += gain * amt
				elif option["position"] == "short":
					num_puts -= amt 
					gain = min(exercise_price - price + prem, prem)
					profit += gain * amt
		x.append(exercise_price)
		y.append(profit)
	
	# Determine the endpoints
	x.append(x[-1] + ENDPOINT_EXTENSION)
	x.insert(0, x[0] - ENDPOINT_EXTENSION)
	y.append(y[-1] + num_calls * ENDPOINT_EXTENSION)
	y.insert(0, y[0] + num_puts * ENDPOINT_EXTENSION)

	return (x, y)

options.sort(key=lambda option: option["price"])
fig = go.Figure()
(x, y) = process_options(options)
fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers"))
fig.add_hline(y=0)
fig.show()
