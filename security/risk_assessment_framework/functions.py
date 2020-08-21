import math
import sys
import csv


def get_threats_occurrence_probability(threats):
    threats['un-normalized_probability'] = threats.apply(lambda row: row.capacity + row.opportunity + row.motivation,
                                                         axis=1)
    return threats


def get_combined_risk_assessment(threats, impact_by_attack, attack_goal, scenario, impact):

    p_r_max = threats.query('attack_goal==@attack_goal and scenario==@scenario')['un-normalized_probability'].max()
    i_m = impact_by_attack.query('attack_goals==@attack_goal')[impact]
    combined_risk_assessment = i_m * p_r_max

    if math.isnan(combined_risk_assessment.iloc[0]):
        print("The scenario {} does not exist in the attack goal {}".format(scenario,attack_goal))
        sys.exit()
    return combined_risk_assessment


def get_risk_characterization(combined_risk_assessment):
    if combined_risk_assessment >= 36:
        risk_treatment = 'refuse'
    elif 24 <= combined_risk_assessment < 36:
        risk_treatment = 'manage'
    elif 12 < combined_risk_assessment < 24:
        risk_treatment = 'accept'
    else:
        risk_treatment = 'accept'
    return risk_treatment


def get_risk_characterization_table(threats, impact_by_attack):
    attack_goals = ['G1', 'G2', 'G3', 'G4', 'G5']
    scenarios = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'S11', 'S12', 'S13', 'S14', 'S15', 'S16',
                 'S17', 'S18', 'S19', 'S20', 'S21', 'S22']
    impacts = ['monetary', 'privacy', 'integrity', 'trust']

    with open('supporting_files/combined_risk_assessment_table.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Attack Goal", "Scenario", "Monetary", "Risk", "Privacy", "Risk", "Integrity", "Risk",
                         "Trust", "Risk"])
        for attack_goal in attack_goals:
            for scenario in scenarios:
                row = []
                p_r_max = threats.query('attack_goal==@attack_goal and scenario==@scenario')['un-normalized_' \
                                                                                             'probability'].max()
                if math.isnan(p_r_max):
                    continue
                row.append(attack_goal)
                row.append(scenario)
                for impact in impacts:
                    i_m = impact_by_attack.query('attack_goals==@attack_goal')[impact]
                    combined_risk_assessment = i_m * p_r_max
                    risk = get_risk_characterization(combined_risk_assessment.iloc[0])
                    row.append(combined_risk_assessment.iloc[0])
                    row.append(risk)
                writer.writerow(row)




