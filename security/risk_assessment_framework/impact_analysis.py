import pandas as pd
from security.risk_assessment_framework.functions import get_threats_occurrence_probability, \
    get_combined_risk_assessment, get_risk_characterization, get_risk_characterization_table

impact_by_attack = pd.read_csv("supporting_files/impact_by_attack.csv")
threats = pd.read_csv("supporting_files/threats.csv")
get_threats_occurrence_probability(threats)

# Combined risk assessment Table 13
attack_goal = 'G3'
scenario = 'S1'
impact = 'monetary'
combined_risk_assessment = get_combined_risk_assessment(threats, impact_by_attack, attack_goal, scenario, impact)
# Risk treatment Table 12
risk_treatment = get_risk_characterization(combined_risk_assessment.iloc[0])
print("For the attack goal {}, scenario {} and {} impact".format(attack_goal, scenario, impact))
print("The combined risk assessment is {}, {} the risk".format(combined_risk_assessment.iloc[0], risk_treatment))

# Get complete table and save it on a csv
get_risk_characterization_table(threats, impact_by_attack)


























