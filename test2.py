import numpy as np

# Define the number of particles
k = 20

# Define the robot motion model (in this case, a simple random walk)
def motion_model(x_prev):
    return x_prev + np.random.normal(0, 0.1, x_prev.shape)

# Define the importance function (in this case, a simple Gaussian distribution)
def importance_function(x, z_measurement):
    return 0.3 * np.random.normal(2, 1, k)# + 0.4 * np.random.normal(5, 2, k) + 0.3 * np.random.normal(9, 1, k)

# Initialize particles uniformly over the state space
particles = np.random.uniform(0, 10, k)

# Simulate sensor measurements (in this case, a known ground truth)
true_pose = 5.0
measurements = np.random.normal(true_pose, 0.1, k)

# Initialize weights for each particle
weights = np.ones(k)

# Number of resampling steps
num_resampling_steps = 1

# SIR algorithm loop
for step in range(num_resampling_steps):
    # Predict the next particle positions using the motion model
    particles = motion_model(particles)
    
    # Calculate importance weights based on sensor measurements
    weights *= importance_function(particles, measurements[step])
    
    # Normalize the weights
    weights /= np.sum(weights)
    
    # Resample particles based on weights
    indices = np.random.choice(range(k), k, p=weights)
    particles = particles[indices]
    weights = np.ones(k) / k

# Estimate the robot pose using the weighted particles
estimated_pose = np.sum(particles * weights)

print(f"True Robot Pose: {true_pose}")
print(f"Estimated Robot Pose: {estimated_pose}")
