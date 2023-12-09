#Simple script to calculate kappa for T decays. 
#Can be modified easily for different decays.
#kappa calculation for T->HT at G/M = %%

import numpy as np
import sympy as sp

# Define numerical values for variables
d_V = 1
X_L = 0
X_R = 1
e_over_sw = np.sqrt(2)*0.458486
m_q = 172.76	#t mass
m_H = 125.35	#Higgs mass
BR = 0.25 # for T->Ht
M_boson = m_H
# Define symbolic variables
M_X, Gamma, kappa, lambda_ = sp.symbols('M_X Gamma kappa lambda_', real = True)

# Define the Gamma expression
#gamma_eq = sp.Eq(8/246**2*M_W**2/e_over_sw**2* d_V * (kappa**2*X_L + kappa**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/M_boson**2 - 2*M_boson**2 - 12*kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R)), Gamma )
gamma_eq = sp.Eq(M_X**2/246**2*    3 * (kappa**2*X_L + kappa**2*X_R) * lambda_ / (96 * np.pi * M_X**3) * (m_q**2 + M_X**2 - M_boson**2 + 4 * kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R)), BR*Gamma) #T->Ht 


#gamma_arr = sp.lambdify((M_X, Gamma, kappa), gamma_eq)
# Solve for kappa
solutions = sp.solve(gamma_eq, kappa)
print("Solutions for kappa:")
for sol in solutions:
    print(sol.evalf()) #gives 2 solutions. We take the +ve solution.

kappa_sol = sp.lambdify((M_X, Gamma, lambda_), solutions[1])

M_X_arr = np.array([700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])  #Array for M_X
#Gamma_arr = np.array([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  #Array for G/M = 1%
Gamma_arr = np.array([35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100])  # Array for G/M = 5%
m1 = m_q
m2 = M_X_arr
m3 = m_H
lambda_arr = np.sqrt(m1**4-2*m1**2*m2**2+m2**4-2*m1**2*m3**2-2*m2**2*m3**2+m3**4)

kappa_arr = kappa_sol(M_X_arr, Gamma_arr, lambda_arr)

# Display the numeric result
print("M_X	Gamma	kappa(T->Ht)")
for M_X_arr, Gamma_arr, kappa_arr in zip(M_X_arr, Gamma_arr, kappa_arr):
    print(f"{M_X_arr}	{Gamma_arr}	{kappa_arr}")
