import math
import sys
import csv


def get_threats_occurrence_probability(threats):
    """
    Compute the probability of occurrence of identified threats for each attack goal and scenario. See Tables 7-11 in
    the paper
    :param threats: data frame containing the threats for each attack goal and scenario.
    :return: dataframe containing the probability of occurrence of identified threats for each attack goal and scenario
    """
    threats['un-normalized_probability'] = threats.apply(lambda row: row.capacity + row.opportunity + row.motivation,
                                                         axis=1)
    return threats


def get_combined_risk_assessment(threats, impact_by_attack, attack_goal, scenario, impact):
    """
    Compute the the combined risk assessment of the attack goal at the scenario with the selected impact. See table 12
    in the paper
    :param threats: dataframe containing the probability of occurrence of identified threats for each attack goal
                    and scenario
    :param impact_by_attack: dataframe containing the impacts for each attack goal
    :param attack_goal: attack goal
    :param scenario: scenario
    :param impact: impact on the attack goal
    :return: the combined risk assessment of the attack goal at the scenario with the selected impact
    """
    p_r_max = threats.query('attack_goal==@attack_goal and scenario==@scenario')['un-normalized_probability'].max()
    i_m = impact_by_attack.query('attack_goals==@attack_goal')[impact]
    combined_risk_assessment = i_m * p_r_max

    if math.isnan(combined_risk_assessment.iloc[0]):
        print("The scenario {} does not exist in the attack goal {}".format(scenario,attack_goal))
        sys.exit()
    return combined_risk_assessment


def get_risk_characterization(combined_risk_assessment):
    """
    Compute the risk characterization for the combined risk assessment. See table 12
    :param combined_risk_assessment: combined risk assessment of the attack goal at the scenario with the selected impact
    :return: risk characterization for the combined risk assessment
    """
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
    """
    Compute the risk characterization table for all attack goals at all scenarios and impacts. See table 13
    in the paper
    :param threats: dataframe containing the probability of occurrence of identified threats for each attack goal
                    and scenario
    :param impact_by_attack: dataframe containing the impacts for each attack goal
    :return: Risk characterization table
    """
    attack_goals = ['G_1', 'G_2', 'G_3', 'G_4', 'G_5']
    scenarios = ['S_1', 'S_2', 'S_3', 'S_4', 'S_5', 'S_6', 'S_7', 'S_8', 'S_9', 'S_{10}', 'S_{11}', 'S_{12}', 'S_{13}',
                 'S_{14}', 'S_{15}', 'S_{16}', 'S_{17}', 'S_{18}', 'S_{19}', 'S_{20}', 'S_{21}', 'S_{22}']
    impacts = ['monetary', 'privacy', 'integrity', 'trust']

    with open('supporting_files/combined_risk_assessment_table.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Attack Goal", "Scenario", "PrMax",
                         "Impact Monetary", "Monetary", "Monetary Risk",
                         "Impact Privacy", "Privacy", "Privacy Risk",
                         "Impact Integrity", "Integrity", "Integrity Risk",
                         "Impact Trust", "Trust", "Trust Risk"])
        for attack_goal in attack_goals:
            for scenario in scenarios:
                row = []
                p_r_max = threats.query('attack_goal==@attack_goal and scenario==@scenario')['un-normalized_' \
                                                                                             'probability'].max()
                if math.isnan(p_r_max):
                    continue
                row.append(attack_goal)
                row.append(scenario)
                row.append(p_r_max)
                for impact in impacts:
                    i_m = impact_by_attack.query('attack_goals==@attack_goal')[impact]
                    combined_risk_assessment = i_m * p_r_max
                    risk = get_risk_characterization(combined_risk_assessment.iloc[0])
                    row.append(i_m.iloc[0])
                    row.append(combined_risk_assessment.iloc[0])
                    row.append(risk)
                writer.writerow(row)




