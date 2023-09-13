import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

k = 20
samples = []

def SIR_Algorithm(k, loops):
    
    x_values = np.linspace(0, 15, k)

    p_x = 0.3 * norm.pdf(x_values, loc=2.0, scale=1.0) + 0.4 * norm.pdf(x_values, loc=5.0, scale=2.0) + 0.3 * norm.pdf(x_values, loc=9.0, scale=1.0)

    q_x = np.random.uniform(0, 15, k) 

    weights = np.ones(k) / k

    plt.plot(x_values, p_x, label='True distribution')
    plt.scatter(q_x, np.zeros(k), color='red', marker='.', label='Samples')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('SIR Resampling Algorithm')
    plt.legend()
    plt.grid(True)
    plt.savefig("p_x_k_"+str(k)+"_loops_"+str(loops)+".png")
    plt.show()

    # SIR Algorithm
    for step in range(loops):
        q_x += np.random.normal(0, 0.2, k) # Predict the next particle positions 
        weights *= np.interp(q_x, x_values, p_x) # Calculate importance weights based on the true distribution
        weights /= np.sum(weights)  # Normalize the weights
        # Resample particles based on weights
        indices = np.random.choice(range(k), k, p=weights)
        q_x = q_x[indices]
        weights = np.ones(k) / k

    plt.plot(x_values, p_x, label='p(x)')
    plt.hist(q_x, x_values, True, 0.5, color='blue', label='Estimated Distribution')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('SIR Resampling Algorithm with Estimated Distribution')
    plt.legend()
    plt.grid(True)
    plt.savefig("p_x_k_"+str(k)+"_loops_"+str(loops)+"_2.png")
    plt.show()

SIR_Algorithm(20, 1)
SIR_Algorithm(100, 1)
SIR_Algorithm(1000, 1)