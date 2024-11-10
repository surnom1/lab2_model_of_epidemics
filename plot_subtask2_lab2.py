import matplotlib.pyplot as plt
import numpy as np

# Define parameters
Lambda, mu, alpha1, alpha2 = 0.002, 0.001, 0.01, 0.1
h = 0.01  # step size

# Initial conditions
S0, E0, I10, I20, R0, N0 = 0.9, 0.05, 0.05, 0.05, 0, 1

# Define the differential equations
def dS(S, E, N, beta): return Lambda - beta*S*E/N - mu*S
def dE(S, E, N, I1, I2, beta, kappa1, kappa2): return beta*S*E/N - (kappa1*I1 + kappa2*I2 + mu)*E
def dI1(E, I1, kappa1, gamma): return kappa1*I1*E - (mu + gamma)*I1 - alpha1*I1
def dI2(E, I1, I2, kappa2, gamma): return kappa2*I2*E + gamma*I1 - mu*I2 - alpha2*I2
def dR(I1, I2, R): return alpha1*I1 + alpha2*I2 - mu*R

def calculate_R0(E, kappa1, kappa2, mu, alpha1, alpha2, gamma):
    term1 = E * (kappa1 * (mu + alpha2) + kappa2 * (mu + gamma + alpha1)) / (2 * (mu + gamma + alpha1) * (mu + alpha2))
    term2 = np.sqrt((term1 ** 2) - kappa1 * kappa2 * E ** 2)
    return term1 + term2

# Values to iterate over
betas = [0.1, 0.25, 0.5]
kappas = [0.1, 0.25, 0.5]
gamma = 0.1
# Create a new plot for each combination of beta, kappa1, kappa2, and gamma
for beta in betas:
    for kappa1 in kappas:
        for kappa2 in kappas:
            S, E, I1, I2, R, N, R_0 = [S0], [E0], [I10], [I20], [R0], [N0], [calculate_R0(E0, kappa1, kappa2, mu, alpha1, alpha2, gamma)]
            
            for t in range(50000):
                
                S.append(S[-1] + h*dS(S[-1], E[-1], N[-1], beta))
                E.append(E[-1] + h*dE(S[-1], E[-1], N[-1], I1[-1], I2[-1], beta, kappa1, kappa2))
                I1.append(I1[-1] + h*dI1(E[-1], I1[-1], kappa1, gamma))
                I2.append(I2[-1] + h*dI2(E[-1], I1[-1], I2[-1], kappa2, gamma))
                R.append(R[-1] + h*dR(I1[-1], I2[-1], R[-1]))
                N.append(S[-1]+ E[-1]+ I1[-1]+ I2[-1]+ R[-1])
                R_0.append(calculate_R0(E[-1], kappa1, kappa2, mu, alpha1, alpha2, gamma))

            # Plot the results
            plt.figure(figsize=(10, 6))
            plt.plot(S, label='S')
            plt.plot(E, label='E')
            plt.plot(I1, label='I1')
            plt.plot(I2, label='I2')
            plt.plot(R, label='R')
            plt.plot(N, label='N')
            plt.plot(R_0, label='R_0')
            plt.title(f'beta={beta}, kappa1={kappa1}, kappa2={kappa2}, gamma={gamma}, lambda={Lambda}, mu={mu}, alpha1={alpha1}, alpha2={alpha2}')
            plt.legend()
            plt.show()