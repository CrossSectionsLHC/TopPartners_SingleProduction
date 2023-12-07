#singlet VLQ 
#calculates Gamma (widths) from kappa (couplings) 
import numpy as np

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
kappa_arr = np.array([0.18, 0.16, 0.14, 0.13, 0.11, 0.10, 0.10, 0.09, 0.08, 0.08, 0.07, 0.07, 0.07, 0.06])  # Array for Kappa
#kappa_arr = np.array([0.276, 0.236, 0.206, 0.184, 0.165, 0.151, 0.138, 0.128, 0.119, 0.111, 0.105, 0.099, 0.093, 0.089])
e_over_sw = np.sqrt(2)*0.458486

# Initialize a dictionary to store results
results_dict = {'M_B': M_X_arr, 'Kappa': kappa_arr}

def Gamma_eqn(decay, M_X, m_q, M_boson, kappa, lambda_):
	if decay == "B->Wt":
	    # Define the Gamma expression
	    gamma_eq = 8/246**2*M_W**2/e_over_sw**2*   d_V * (kappa**2*X_L + kappa**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/M_boson**2 - 2*M_boson**2 - 12*kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R))	
	if decay == "B->Zb":
	    # Define the Gamma expression
	    gamma_eq = 4/246**2*M_W**2/e_over_sw**2*   d_V * (kappa**2*X_L + kappa**2*X_R)*3/4*(e_over_sw)**2*lambda_/(96*np.pi*M_X**3)*(m_q**2 + M_X**2 + (m_q**4 - 2*m_q**2*M_X**2 + M_X**4)/M_boson**2 - 2*M_boson**2 - 12*kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R))
	elif decay == "B->Hb":
	    # Define the Gamma expression
	    gamma_eq = M_X**2/246**2 *3 * (kappa**2*X_L + kappa**2*X_R) * lambda_ / (96 * np.pi * M_X**3) * (m_q**2 + M_X**2 - M_boson**2 + 4 * kappa**2*X_L*kappa**2*X_R*m_q*M_X/(kappa**2*X_L + kappa**2*X_R))
	return gamma_eq

X_decays = ["B->Wt", "B->Zb", "B->Hb"]	
for decay in X_decays:
    if decay == "B->Wt":
        m1 = m_t
        m2 = M_X_arr
        m3 = M_W
    elif decay == "B->Zb":
        m1 = m_b
        m2 = M_X_arr
        m3 = M_Z
    elif decay == "B->Hb":
        m1 = m_b
        m2 = M_X_arr
        m3 = M_H
    lambda_arr = np.sqrt(m1**4 - 2*m1**2*m2**2 + m2**4 - 2*m1**2*m3**2 - 2*m2**2*m3**2 + m3**4)
    Gamma_arr = Gamma_eqn(decay, M_X_arr, m1, m3, kappa_arr, lambda_arr)
    # Store results in the dictionary
    results_dict[f'Gamma({decay})'] = Gamma_arr
    

# Display the numeric results in a table
results_table = np.column_stack(tuple(results_dict.values()))
header = [key for key in results_dict.keys()]

header.append("Gamma(Total)")
print("\t".join(header))
i = 0
for row in results_table:
    print("\t".join(map(str, row)),"\t", results_dict["Gamma(B->Wt)"][i]+results_dict["Gamma(B->Zb)"][i]+results_dict["Gamma(B->Hb)"][i])
    i=i+1
