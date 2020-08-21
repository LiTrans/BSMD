import pandas as pd
from security.risk_assessment_framework.functions import get_threats_occurrence_probability, \
    get_combined_risk_assessment

impact_by_attack = pd.read_csv("supporting_files/impact_by_attack.csv")
threats = pd.read_csv("supporting_files/threats.csv")
get_threats_occurrence_probability(threats)

# Combined risk assessment
combined_risk_assessment = get_combined_risk_assessment(threats, impact_by_attack, 'G3', 'S11', 'monetary')
print(combined_risk_assessment)




























