
import matplotlib.pyplot as plt
from Engine import Game
import numpy as np

n_games = 10000
n_shots = []
n_wins1 = 0
n_wins2 = 0

for i in range(n_games):
    game = Game(human1=False, human2=False)
    while not game.over:
        if game.player1_turn:
            game.benchmark_ai()
        else:
            game.benchmark_ai()
    n_shots.append(game.n_shots)
    if game.result == 1:
        n_wins1 += 1
    elif game.result == 2:
        n_wins2 += 1


print(n_wins1)
print(n_wins2)


values = []
for i in range(17, 200):
    values.append(n_shots.count(i))


median_value = np.median(n_shots)
mean_value = np.mean(n_shots)


plt.figure(figsize=(10, 6))
bars = plt.bar(range(17, 200), values, color='skyblue', label='Number of shots')

# Dodanie orientacyjnej mediany i średniej
plt.axvline(x=median_value, color='red', linestyle='--', linewidth=2, label='Median', alpha=0.5)
plt.axvline(x=mean_value, color='green', linestyle='--', linewidth=2, label='Mean', alpha=0.5)

plt.title('Number of shots per game', fontsize=14)
plt.xlabel('Number of shots', fontsize=12)
plt.ylabel('Number of games', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()