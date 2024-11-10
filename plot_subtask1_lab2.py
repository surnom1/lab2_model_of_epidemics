import matplotlib.pyplot as plt

# Define the parameters
Lambda = 0.02
mu = 0.01
alpha1 = 0.1
alpha2 = 0.1
betas = [0.25, 0.5, 0.75]
gammas = [0.25, 0.5, 0.75]

# Define the initial conditions
S0 = 0.9
I10 = 0.05
I20 = 0.05
R0 = 0.0
N0 = S0 + I10 + I20 + R0

def calculate_R0(beta, gamma):
    return (beta*S0)/((gamma+alpha1+mu)*N0)

# Define the time step
h = 0.01

# Define the functions for the derivatives
def dS(S, I1, N, beta): return Lambda - beta*S*I1/N - mu*S
def dI1(S, I1, N, beta, gamma): return beta*S*I1/N - (mu + gamma)*I1 - alpha1*I1
def dI2(I1, I2, gamma): return gamma*I1 - mu*I2 - alpha2*I2
def dR(I1, I2, R): return alpha1*I1 + alpha2*I2 - mu*R

# Create a new plot for each combination of beta and gamma
for beta in betas:
    for gamma in gammas:
        S, I1, I2, R, N = [S0], [I10], [I20], [R0], [N0]
        R_0 = calculate_R0(beta, gamma)
        for t in range(50000):
            S.append(S[-1] + h*dS(S[-1], I1[-1], N[-1], beta))
            I1.append(I1[-1] + h*dI1(S[-1], I1[-1], N[-1], beta, gamma))
            I2.append(I2[-1] + h*dI2(I1[-1], I2[-1], gamma))
            R.append(R[-1] + h*dR(I1[-1], I2[-1], R[-1]))
            N.append(S[-1] + I1[-1] + I2[-1] + R[-1])

        # Plot the results
        plt.figure(figsize=(10, 6))
        plt.plot(S, label='S')
        plt.plot(I1, label='I1')
        plt.plot(I2, label='I2')
        plt.plot(R, label='R')
        plt.plot(N, label='N')
        plt.title(f'beta={beta:.3f}, gamma={gamma:.3f}, R0={R_0:.3f}, lambda={Lambda:.3f}, mu={mu:.3f}, alpha1={alpha1:.3f}, alpha2={alpha2:.3f}')
        plt.legend()
        plt.show()
plt.plot(N, label='N')
plt.legend()
plt.show()