import pandas as pd

def parse_excel(file_path):
    # Load the Excel file
    excel_data = pd.ExcelFile(file_path)
    sheet1 = pd.read_excel(excel_data, sheet_name='Sheet1', header=None)
    sheet2 = pd.read_excel(excel_data, sheet_name='Sheet2', header=None)

    # ===== Sheet1 Processing =====
    # Extract day numbers and day names
    day_numbers = sheet1.iloc[0, 1:].tolist()
    day_names = sheet1.iloc[1, 1:].tolist()

    # Extract employee data (starting from row 3)
    employee_data = sheet1.iloc[3:].reset_index(drop=True)

    # Filter out rows that are roles, not employees
    employee_data = employee_data[employee_data[0].str.contains("Employee", na=False)]

    # Debug: Print employee_data to validate structure
    print("Filtered Employee Data:\n", employee_data.head())

    # Assign employees to skill categories
    skill_mapping = {
        "Lab Tech III": list(employee_data.iloc[0:3, 0]),  # Employees 1-3
        "Lab Tech II": list(employee_data.iloc[4:12, 0]),  # Employees 4-12
        "Lab Tech I": list(employee_data.iloc[12:16, 0])   # Employees 13-16
    }

    # Debug: Print skill mapping for validation
    print("Skill Mapping:\n", skill_mapping)

    # ===== Sheet2 Processing =====
    # Extract day numbers and day names from Sheet2
    shift_headers = sheet2.iloc[1, 1:].tolist()  # Day numbers (e.g., 1, 2, 3)
    day_names_sheet2 = sheet2.iloc[2, 1:].tolist()  # Day names (e.g., SU, M, TU)

    # Initialize storage for parsed data
    shifts_needed = {}

    # Identify the hierarchical structure of roles and locations
    current_role = None
    for index, row in sheet2.iterrows():
        if index < 3:  # Skip the first three rows (headers)
            continue

        # Detect role (Lab Tech III, Lab Tech II, Lab Tech I)
        if pd.notna(row[0]) and "Lab Tech" in str(row[0]):  
            current_role = row[0].strip()  # Set current role and strip excess spaces
            shifts_needed[current_role] = {}  # Initialize dictionary for this role
        elif current_role:  # Process locations under the current role
            location = str(row[0]).strip()  # Location name
            if pd.notna(location):  # Ensure location is valid
                shift_data = row[1:].tolist()  # Shift data for this location
                shifts_needed[current_role][location] = shift_data

    # Debug: Print parsed data for Sheet2
    print("Shift Headers (Day Numbers):\n", shift_headers)
    print("Day Names (Sheet2):\n", day_names_sheet2)
    print("Shifts Needed (Processed):\n", shifts_needed)

    return day_numbers, day_names, skill_mapping, shifts_needed
