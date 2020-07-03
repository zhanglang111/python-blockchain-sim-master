import numpy as np
import matplotlib.pyplot as plt

mu = 80  #期望为1
sigma = 4  #标准差为3
num = 100  #个数为10000

rand_data = np.random.normal(mu, sigma, num)
bins = range(60,100)
plt.hist(rand_data,bins)
plt.show()