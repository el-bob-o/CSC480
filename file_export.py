from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import pandas as pd

def save_schedule_to_excel(schedule, day_numbers, day_names):
    Tk().withdraw()  # Hide the root Tkinter window
    file_path = asksaveasfilename(
        title="Save Schedule",
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")]
    )
    if not file_path:
        print("Save cancelled.")
        return

    # Combine day numbers and day names for headers
    headers = [f"{name} ({num})" for name, num in zip(day_names, day_numbers)]
    cleaned_schedule = schedule.copy()
    cleaned_schedule.columns = headers

    # Export to Excel
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        cleaned_schedule.to_excel(writer, index=True, sheet_name="Schedule")

    print(f"Schedule saved to {file_path}")
