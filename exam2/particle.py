import numpy as np
import random_numbers as rn
import math

SD_dist = 20
SD_angle = 0.05

class Particle(object):
    """Data structure for storing particle information (state and weight)"""
    def __init__(self, x=0.0, y=0.0, theta=0.0, weight=0.0):
        self.x = x
        self.y = y
        self.theta = np.mod(theta, 2.0*np.pi)
        self.weight = weight

    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def getTheta(self):
        return self.theta
        
    def getWeight(self):
        return self.weight

    def setX(self, val):
        self.x = val

    def setY(self, val):
        self.y = val

    def setTheta(self, val):
        self.theta = np.mod(val, 2.0*np.pi)

    def setWeight(self, val):
        self.weight = val


def estimate_pose(particles_list):
    """Estimate the pose from particles by computing the average position and orientation over all particles. 
    This is not done using the particle weights, but just the sample distribution."""
    x_sum = 0.0
    y_sum = 0.0
    cos_sum = 0.0
    sin_sum = 0.0
     
    for particle in particles_list:
        x_sum += particle.getX()
        y_sum += particle.getY()
        cos_sum += np.cos(particle.getTheta())
        sin_sum += np.sin(particle.getTheta())
        
    flen = len(particles_list)
    if flen != 0:
        x = x_sum / flen
        y = y_sum / flen
        theta = np.arctan2(sin_sum/flen, cos_sum/flen)
    else:
        x = x_sum
        y = y_sum
        theta = 0.0
        
    return Particle(x, y, theta)
     
     
def move_particle(particle, delta_x, delta_y, delta_theta):
    """Move the particle by (delta_x, delta_y, delta_theta)"""
    particle.x += delta_x
    particle.y += delta_y
    particle.theta += delta_theta


def add_uncertainty(particles_list, sigma, sigma_theta):
    """Add some noise to each particle in the list. Sigma and sigma_theta is the noise
    variances for position and angle noise."""
    for particle in particles_list:
        particle.x += rn.randn(0.0, sigma)
        particle.y += rn.randn(0.0, sigma)
        particle.theta = np.mod(particle.theta + rn.randn(0.0, sigma_theta), 2.0 * np.pi) 


def add_uncertainty_von_mises(particles_list, sigma, theta_kappa):
    """Add some noise to each particle in the list. Sigma and theta_kappa is the noise
    variances for position and angle noise."""
    for particle in particles_list:
        particle.x += rn.randn(0.0, sigma)
        particle.y += rn.randn(0.0, sigma)
        particle.theta = np.mod(rn.rand_von_mises(particle.theta, theta_kappa), 2.0 * np.pi) - np.pi

def d_i(x_offset, x_value, y_offset, y_value):
    return np.sqrt(((x_offset - x_value) ** 2) + ((y_offset - y_value) ** 2))

def e_l(x_offset, x_value, y_offset, y_value):
    return np.array([x_offset - x_value, y_offset - y_value]).T / (d_i(x_offset, x_value, y_offset, y_value))

def e_theta(theta):
    return np.array([-np.sin(theta), np.cos(theta)]).T

def fi_i(el, etheta):
    return np.sign(np.dot(el, etheta) * np.arccos(np.dot(el, etheta)))

def distance_weight(measured_distance,x_offset, x_value, y_offset, y_value, di):
    return (1/np.sqrt(2*np.pi* (SD_dist ** 2)))* np.exp(-((measured_distance - di) ** 2) / (2 * SD_dist ** 2))

def angle_weight(measure_angle, fii):
    return (1/np.sqrt(2*np.pi* (SD_angle ** 2)))* np.exp(-((measure_angle - fii) ** 2) / (2 * SD_angle ** 2))