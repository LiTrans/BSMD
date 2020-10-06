import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

from security.risk_assessment_framework.functions import get_threats_occurrence_probability, \
    get_combined_risk_assessment, get_risk_characterization, get_risk_characterization_table

impact_by_attack = pd.read_csv("supporting_files/impact_by_attack.csv")
threats = pd.read_csv("supporting_files/threats.csv")
get_threats_occurrence_probability(threats)

"""
Example of the combined risk assessment for a specific attack goal at a specific scenario and impact
This simple calculator computes P(G_i,S_j,A_k)=c(G_i,S_j,A_k) + o(G_i,S_j,A_k) + m(G_i,S_j,A_k) for a given
G_i, S_j and A_k. See Equation 3 on the paper
"""
attack_goal = 'G_3'
scenario = 'S_1'
impact = 'monetary'
combined_risk_assessment = get_combined_risk_assessment(threats, impact_by_attack, attack_goal, scenario, impact)
risk_treatment = get_risk_characterization(combined_risk_assessment.iloc[0])
print("For the attack goal {}, scenario {} and {} impact".format(attack_goal, scenario, impact))
print("The combined risk assessment is {}, {} the risk".format(combined_risk_assessment.iloc[0], risk_treatment))

"""
Create the risk characterization table for all attack goals at all scenarios and impacts.
Compute P(G_i,S_j,A_k) for all i,j and k and stores the results in the combined_risk_assessment.csv. 
See Appendix C on the paper
"""
get_risk_characterization_table(threats, impact_by_attack)


"""
The results of the actor-based risk analysis for all attack goals at its corresponded scenario. 
Each graph correspond to an attack goal, G_i, and its associated scenarios, S_j. 
The bars indicate R_T(G_i,S_j), i.e., the associated risk for a given attack goal, scenario and impact
type. The figure is saved in the supporting_file folder. See Figure 8 on the paper
"""
goals = pd.read_csv("supporting_files/combined_risk_assessment_table.csv", usecols=(0,1,4,7,10,13))
G1 = goals.loc[goals['Attack Goal'] == 'G_1']
G2 = goals.loc[goals['Attack Goal'] == 'G_2']
G3 = goals.loc[goals['Attack Goal'] == 'G_3']
G4 = goals.loc[goals['Attack Goal'] == 'G_4']
G5 = goals.loc[goals['Attack Goal'] == 'G_5']

fig1 = plt.figure(figsize=(15, 13))
gs = gridspec.GridSpec(3, 3, width_ratios=[4, 4, 5])
gs.update(wspace=0.05, hspace=0.25)

# G1
f1_ax1 = plt.subplot(gs[0, :-2])
G1_ax = G1.plot(kind="bar", color=['m', 'blue', 'brown', 'cyan'], edgecolor='white', width=.8, ax=f1_ax1)
plt.legend(prop={'size': 16})
G1_ax.set_ylim([0, 50])
x = np.arange(-1,10,0.1)
negligible = 12
acceptable = 23
undesirable = 35
unacceptable = 50
G1_ax.set_title(r'$G_1$', fontsize=18)
plt.xticks(range(0, len(G1['Scenario'])),  r'$' + G1['Scenario'] + '$', rotation=0, fontsize=15)
plt.yticks(fontsize=15)
G1_ax.fill_between(x, unacceptable, color='r')
G1_ax.fill_between(x, undesirable, color=(0.886, 0.424, 0.031))
G1_ax.fill_between(x, acceptable, color=(1, 0.949, 0))
G1_ax.fill_between(x, negligible, color=(0, 0.686, 0.314))

# G2
f1_ax2 = plt.subplot(gs[0, 1:-1])
G2_ax = G2.plot(kind="bar", color=['m', 'blue', 'brown', 'cyan'], edgecolor='white', width=.8, ax=f1_ax2)
G2_ax.set_ylim([0, 50])
x = np.arange(-1,10,0.1)
negligible = 12
acceptable = 23
undesirable = 35
unacceptable = 50
G2_ax.set_title(r'$G_2$', fontsize=18)
plt.xticks(range(0, len(G2['Scenario'])), r'$' + G2['Scenario'] + '$', rotation=0, fontsize=15)
G2_ax.tick_params(labelleft=False)
G2_ax.get_legend().remove()
G2_ax.fill_between(x, unacceptable, color='r')
G2_ax.fill_between(x, undesirable, color=(0.886, 0.424, 0.031))
G2_ax.fill_between(x, acceptable, color=(1, 0.949, 0))
G2_ax.fill_between(x, negligible, color=(0, 0.686, 0.314))

#G3
f1_ax3 = plt.subplot(gs[0, 2:])
G3_ax = G3.plot(kind="bar", color=['m', 'blue', 'brown', 'cyan'], edgecolor='white', width=.8, ax=f1_ax3)
G3_ax.set_ylim([0, 50])
x = np.arange(-1,10,0.1)
negligible = 12
acceptable = 23
undesirable = 35
unacceptable = 50
G3_ax.set_title(r'$G_3$', fontsize=18)
plt.xticks(range(0, len(G3['Scenario'])), r'$' + G3['Scenario'] + '$', rotation=0, fontsize=15)
G3_ax.tick_params(labelleft=False)
G3_ax.get_legend().remove()
G3_ax.fill_between(x, unacceptable, color='r')
G3_ax.fill_between(x, undesirable, color=(0.886, 0.424, 0.031))
G3_ax.fill_between(x, acceptable, color=(1, 0.949, 0))
G3_ax.fill_between(x, negligible, color=(0, 0.686, 0.314))

# G4
f1_ax4 = plt.subplot(gs[1, :])
G4_ax = G4.plot(kind="bar", color=['m', 'blue', 'brown', 'cyan'], edgecolor='white', width=.8, ax=f1_ax4)
G4_ax.set_ylim([0, 50])
x = np.arange(-1,22,0.1)
negligible = 12
acceptable = 23
undesirable = 35
unacceptable = 50
G4_ax.set_title(r'$G_4$', fontsize=18)
plt.xticks(range(0, len(G4['Scenario'])), r'$' + G4['Scenario'] + '$', rotation=0, fontsize=15)
plt.yticks(fontsize=15)
G4_ax.get_legend().remove()
G4_ax.fill_between(x, unacceptable, color='r')
G4_ax.fill_between(x, undesirable, color=(0.886, 0.424, 0.031))
G4_ax.fill_between(x, acceptable, color=(1, 0.949, 0))
G4_ax.fill_between(x, negligible, color=(0, 0.686, 0.314))

# G5
f1_ax5 = plt.subplot(gs[2, :])
G5_ax = G5.plot(kind="bar", color=['m', 'blue', 'brown', 'cyan'], edgecolor='white', width=.8, ax=f1_ax5)
G5_ax.set_ylim([0, 50])
x = np.arange(-1,22,0.1)
negligible = 12
acceptable = 23
undesirable = 35
unacceptable = 50
G5_ax.set_title(r'$G_5$', fontsize=18)
plt.xticks(range(0, len(G5['Scenario'])), r'$' + G5['Scenario'] + '$', rotation=0, fontsize=15)
plt.yticks(fontsize=15)
G5_ax.get_legend().remove()
G5_ax.fill_between(x, unacceptable, color='r')
G5_ax.fill_between(x, undesirable, color=(0.886, 0.424, 0.031))
G5_ax.fill_between(x, acceptable, color=(1, 0.949, 0))
G5_ax.fill_between(x, negligible, color=(0, 0.686, 0.314))

fig1.text(0.075, 0.5, 'Risk assessment, ' + r'$R_T(G_i,S_j)$', rotation="vertical", va="center", fontsize=18)
fig1.text(0.5, 0.070 , 'Scenarios, ' + r'$S_j$', va="center", fontsize=18)
plt.savefig("supporting_files/risk_assessment.png", dpi=300, bbox_inches = 'tight', pad_inches = 0.05)



























