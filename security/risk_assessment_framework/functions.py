

def get_threats_occurrence_probability(threats):
    threats['un-normalized_probability'] = threats.apply(lambda row: row.capacity + row.opportunity + row.motivation,
                                                         axis=1)
    return threats


def get_combined_risk_assessment(threats, impact_by_attack, attack_goal, scenario, impact):
    p_r_max = threats.query('attack_goal==@attack_goal and scenario==@scenario')['un-normalized_probability'].max()
    i_m = impact_by_attack.query('attack_goals==@attack_goal')[impact]
    combined_risk_assessment = i_m * p_r_max
    return combined_risk_assessment

