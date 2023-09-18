import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

k = 20
samples = []

def SIR_Algorithm(k, loops):
    
    x_values = np.linspace(0, 15, k)

    def p(x_values):
        return 0.3 * norm.pdf(x_values, loc=2.0, scale=1.0) + 0.4 * norm.pdf(x_values, loc=5.0, scale=2.0) + 0.3 * norm.pdf(x_values, loc=9.0, scale=1.0)

    def q(x_vals):
        return 1/15
    
    q_x = np.random.normal(5, 4, k)
    

    weights = np.ones(k) / k


    p_x = p(x_values)

    plt.plot(x_values, p_x, label='True distribution')
    plt.scatter(q_x, np.zeros(k), color='red', marker='.', label='Samples')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('SIR Resampling Algorithm')
    plt.legend()
    plt.grid(True)
    plt.savefig("resq2/p_x_k_"+str(k)+"_loops_"+str(loops)+".png")
    plt.show()

    weights = p(q_x) / q(q_x)
    weights /= np.sum(weights)                        # Normalize the weights
    # Resample particles based on weights
    indices = np.random.choice(range(k), k, p=weights)
    q_x = q_x[indices]
    weights = np.ones(k) / k

    plt.plot(x_values, p_x, label='p(x)')
    plt.hist(q_x, x_values, density=True, color='blue', label='Estimated Distribution')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('SIR Resampling Algorithm with Estimated Distribution')
    plt.legend()
    plt.grid(True)
    plt.savefig("resq2/p_x_k_"+str(k)+"_loops_"+str(loops)+"_2.png")
    plt.show()

SIR_Algorithm(20, 1)
SIR_Algorithm(100, 1)
SIR_Algorithm(1000, 1)