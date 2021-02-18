import requests
import config
import matplotlib.pyplot as plt
import numpy as np

values = {0}
resp_history = requests.get(config.urlhistory).json()
for i in resp_history['rates']:
	for j in resp_history['rates'][i]:
		values.add(resp_history['rates'][i][j])
values.remove(0)

x = [1, 2, 3, 4, 5]

fig = plt.figure()
plt.bar(x, values)
plt.title('Simple bar chart')
plt.grid(True)   # линии вспомогательной сетки
fig.savefig('Graph.jpg')