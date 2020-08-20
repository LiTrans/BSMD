

# Monetary impact levels
# 0: No monetary loss
# 1: Minor monetary loss
# 2: Significant monetary loss
# 3: Severe monetary loss
# 4: Catastrophic monetary loss
monetary = [0, 1, 2, 3, 4]

# Privacy impact levels
# 0: No impact on the privacy
# 1: Minor impact on the privacy of any of the nodes in BSMD (Individuals, Companies, Universities and Government)
# 2: Significant on the privacy of the nodes in BSMD
# 3: Severe on the privacy of the nodes in BSMD
# 4: Catastrophic on the privacy of the nodes in BSMD
privacy = [0, 1, 2, 3, 4]

# Integrity impact levels
# 0: No impact on the integrity
# 1: Minor impact on the integrity of the mobility data, transactions and integrity of the users
# 2: Significant impact on the integrity of the mobility data, transactions and integrity of the users
# 3: Severe impact on the integrity of the mobility data, transactions and integrity of the users
# 4: Catastrophic impact on the integrity of the mobility data, transactions and integrity of the users
integrity = [0, 1, 2, 3, 4]

# Trust impact levels
# 0: No impact on the trust
# 1: Minor impact on the trust of the BSMD network
# 2: Significant impact on the trust of the BSMD network
# 3: Severe impact on the trust of the BSMD network
# 4: Catastrophic impact on the trust of the BSMD
trust = [0, 1, 2, 3, 4]

# Impact on the victims by attack goal
# G1-Gain knowledge about the data-market
G1 = [monetary[1], privacy[2], integrity[0], trust[1]]
# G2-Access sensitive data on the nodes of the network
G2 = [monetary[2], privacy[3], integrity[0], trust[2]]
# G3-Manipulate and modify blockchain information
G3 = [monetary[3], privacy[2], integrity[4], trust[4]]
# G4-Sabotage activities
G4 = [monetary[3], privacy[0], integrity[2], trust[3]]
# G5-Induce participants in the blockchain network to make errors
G5 = [monetary[2], privacy[0], integrity[3], trust[3]]



























