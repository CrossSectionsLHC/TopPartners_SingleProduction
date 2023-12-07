import numpy as np
import sympy as sp

# Define numerical values for variables
d_V = 1
X_L = 0
X_R = 1
e_over_sw = np.sqrt(2)*0.458486
m_q = 4.18	#b mass
m_V = 80.37	#W mass
m_H = 125.35	#Higgs mass

M_X, Gamma, k_V, lambda_ = sp.symbols('M_X Gamma k_V lambda_', real = True)

# Define symbolic variables
k_V = sp.symbols('k_V')

# Define the Gamma expression
gamma_eq = sp.Eq( d_V * (k_V**2*X_L + k_V**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/m_V**2 - 2*m_V**2 - 12*k_V**2*X_L*k_V**2*X_R*m_q*M_X/(k_V**2*X_L + k_V**2*X_R)), Gamma )

#gamma_arr = sp.lambdify((M_X, Gamma, k_V), gamma_eq)
# Solve for k_V
solutions = sp.solve(gamma_eq, k_V)
print("Solutions for k_V:")
for sol in solutions:
    print(sol.evalf()) #gives 2 solutions. We take the +ve solution.

k_V_sol = sp.lambdify((M_X, Gamma, lambda_), solutions[1])

M_X_arr = np.array([700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])  #Array for M_X
Gamma_arr = np.array([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  #Array for Gamma
m1 = m_q
m2 = M_X_arr
m3 = m_V
lambda_arr = np.sqrt(m1**4-2*m1**2*m2**2+m2**4-2*m1**2*m3**2-2*m2**2*m3**2+m3**4)

k_V_arr = k_V_sol(M_X_arr, Gamma_arr, lambda_arr)

# Display the numeric result
for M_X_arr, Gamma_arr, k_V_arr in zip(M_X_arr, Gamma_arr, k_V_arr):
    print(f"M_X = {M_X_arr},	Gamma = {Gamma_arr},	k_V = {k_V_arr}")
