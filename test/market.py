import random
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation


class Market:

    def __init__(self):
        self.lightsaber = {"actuel": 200, "juste": 200}
        self.sword = {"actuel": 20, "juste": 20}
        self.gun = {"actuel": 20, "juste": 20}
        self.ammunition = {"actuel": 0.1, "juste": 0.1}

    @classmethod
    def _fluctuation(cls, article: dict):
        if article["actuel"] <= article["juste"] / 10:
            article["actuel"] += random.uniform(0, article["actuel"] / 100)
        elif article["actuel"] >= article["juste"] * 10:
            article["actuel"] += random.uniform(-article["actuel"] / 100, 0)
        else:
            article["actuel"] += random.uniform(-article["actuel"] / 100, article["actuel"] / 100)
        return article

    def fluctuation(self):
        self.lightsaber = self._fluctuation(self.lightsaber)
        self.sword = self._fluctuation(self.sword)
        self.gun = self._fluctuation(self.gun)
        self.ammunition = self._fluctuation(self.ammunition)

    def behavior(self):
        self.fluctuation()


m = Market()
x = []
y = []
while True:
    m.behavior()
    # sleep()
    print(m.lightsaber, m.sword, m.gun, m.ammunition)
    t = datetime.now().time()
    x.append(datetime.now())
    y.append(m.sword["actuel"])

# Create a line plot
    plt.plot(x, y)

# Display the plot
    plt.show()
