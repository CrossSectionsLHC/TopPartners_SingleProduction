#Singlet VLQ
#Calculates Kappa (couplings) from Gamma (width)
import numpy as np
import sympy as sp

# Define numerical values for variables
d_V = 1
X_L = 1
X_R = 0
m_b = 4.18	# b mass
m_t = 172.76	# t mass
M_W = 80.37	# W mass
M_Z = 91.19	# Z mass
M_H = 125.35	# Higgs mass
M_X_arr = np.array([700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000])  # Array for M_X
Gamma_arr = np.array([7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])  # Array for G/M = 1%
e_over_sw = np.sqrt(2)*0.458486

# Define symbolic variables
M_X, m_q, M_boson, Gamma, kappa, lambda_, BR = sp.symbols('M_X m_q M_boson Gamma kappa lambda_ BR', real=True)

# Initialize a dictionary to store results
results_dict = {'M_B': M_X_arr, 'Gamma': Gamma_arr}

X_decays = ["B->Wt", "B->Zb", "B->Hb"]
for decay in X_decays:
    if decay == "B->Wt":
        # Define the Gamma expression
        gamma_eq = sp.Eq(8/246**2*M_W**2/e_over_sw**2*   d_V * (kappa**2*X_L + kappa**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/M_boson**2 - 2*M_boson**2 - 12*kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R)), BR*Gamma)
    elif decay == "B->Zb":
        # Define the Gamma expression
        gamma_eq = sp.Eq(4/246**2*M_W**2/e_over_sw**2*   d_V * (kappa**2*X_L + kappa**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/M_boson**2 - 2*M_boson**2 - 12*kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R)), BR*Gamma)
    elif decay == "B->Hb":
        # Define the Gamma expression
        gamma_eq = sp.Eq(M_X**2/246**2*    3 * (kappa**2*X_L + kappa**2*X_R) * lambda_ / (96 * np.pi * M_X**3) * (m_q**2 + M_X**2 - M_boson**2 + 4 * kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R)), BR*Gamma)
    
    # Solve for kappa
    solutions = sp.solve(gamma_eq, kappa)
    print('Solutions for kappa', decay)
    for sol in solutions:
        print(sol.evalf())  # gives 2 solutions. We take the +ve solution.
    kappa_sol = sp.lambdify((M_X, Gamma, lambda_, m_q, M_boson, BR), solutions[1])

    if decay == "B->Wt":
        m1 = m_t
        m2 = M_X_arr
        m3 = M_W
        br = 0.50
    elif decay == "B->Zb":
        m1 = m_b
        m2 = M_X_arr
        m3 = M_Z
        br = 0.25
    elif decay == "B->Hb":
        m1 = m_b
        m2 = M_X_arr
        m3 = M_H
        br = 0.25
    lambda_arr = np.sqrt(m1**4 - 2*m1**2*m2**2 + m2**4 - 2*m1**2*m3**2 - 2*m2**2*m3**2 + m3**4)
    kappa_arr = kappa_sol(M_X_arr, Gamma_arr, lambda_arr, m1, m3, br)
    # Store results in the dictionary
    results_dict[f'kappa({decay})'] = kappa_arr

# Display the numeric results in a table
results_table = np.column_stack(tuple(results_dict.values()))
header = [key for key in results_dict.keys()]

print("\t".join(header))
for row in results_table:
    print("\t".join(map(str, row)))
