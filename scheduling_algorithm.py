import pandas as pd

def schedule_employees(day_numbers, day_names, skill_mapping, shifts_needed):
    schedule = {}
    weekly_shift_count = {employee: 0 for skill in skill_mapping.values() for employee in skill}
    daily_assigned_employees = {day: set() for day in day_numbers}

    for role, locations in shifts_needed.items():
        schedule[role] = {}

        for location, shifts in locations.items():
            schedule[role][location] = []

            for day_idx, shift in enumerate(shifts):
                if pd.isna(shift) or shift == "HOL":
                    schedule[role][location].append("HOL" if shift == "HOL" else None)
                    continue

                day_number = day_numbers[day_idx]
                day_name = day_names[day_idx]

                week_number = day_idx // 7  # Calculate week index based on day index
                available_employees = skill_mapping.get(role, [])

                assigned = False
                for employee in available_employees:
                    # Check if employee can work this shift
                    if (weekly_shift_count[employee] < 5 and
                            employee not in daily_assigned_employees[day_number]):
                        # Assign employee to shift
                        schedule[role][location].append(f"{employee} ({shift})")
                        weekly_shift_count[employee] += 1
                        daily_assigned_employees[day_number].add(employee)
                        assigned = True
                        break

                if not assigned:
                    schedule[role][location].append("PRN")  # Mark shift as unfilled (PRN)

            # Reset weekly counters every Sunday
            if day_name == "SU":
                weekly_shift_count = {employee: 0 for employee in weekly_shift_count}

    return schedule
