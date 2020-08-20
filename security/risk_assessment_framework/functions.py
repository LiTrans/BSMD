

def threats_occurrence_probability(actor_capacity, actor_opportunity, actor_motivation):
    probability = actor_capacity + actor_opportunity + actor_motivation
    return probability


def combined_risk_assessment(max_probability_per_attack, attack_goal_impact):
    risk = attack_goal_impact * max_probability_per_attack
    return risk