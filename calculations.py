def calculate_HPI(concentrations, standards):
    try:
        # Step 1: calculate weights
        weights = {m: 1 / standards[m] for m in concentrations if m in standards and standards[m] != 0}
        
        # Step 2: calculate Qi for each metal
        q_values = {m: (concentrations[m] / standards[m]) * 100 for m in concentrations if m in standards and standards[m] != 0}
        
        # Step 3: weighted sum
        numerator = sum(q_values[m] * weights[m] for m in q_values)
        denominator = sum(weights.values())
        
        return numerator / denominator if denominator != 0 else None
    except Exception as e:
        print(f"Error in HPI calculation: {e}")
        return None


def calculate_HEI(concentrations, standards):
    try:
        return sum(concentrations[m] / standards[m] for m in concentrations if m in standards and standards[m] != 0)
    except Exception as e:
        print(f"Error in HEI calculation: {e}")
        return None
