from tkinter import messagebox
from data_import import parse_excel
from scheduling_algorithm import schedule_employees
from visualization import visualize_shifts_needed
from file_export import save_schedule_to_excel
import matplotlib.pyplot as plt
import tkinter as tk


class SchedulingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduling Application")
        self.file_path = None
        self.schedule = None
        self.day_numbers = None
        self.day_names = None
        self.skill_mapping = None
        self.shift_data = None

        # GUI Elements
        tk.Button(root, text="Load Excel File", command=self.load_file, width=20).pack(pady=10)
        tk.Button(root, text="Generate Schedule", command=self.generate_schedule, width=20).pack(pady=10)
        tk.Button(root, text="Visualize Schedule", command=self.visualize_schedule, width=20).pack(pady=10)
        tk.Button(root, text="Visualize Imported Sheet2", command=self.visualize_imported_sheet2, width=20).pack(pady=10)
        tk.Button(root, text="Save Schedule", command=self.save_schedule, width=20).pack(pady=10)

    def load_file(self):
        try:
            from tkinter.filedialog import askopenfilename
            self.file_path = askopenfilename(title="Select an Excel file", filetypes=[("Excel files", "*.xlsx")])
            if not self.file_path:
                raise FileNotFoundError("No file selected.")
            self.day_numbers, self.day_names, self.skill_mapping, self.shift_data = parse_excel(self.file_path)
            messagebox.showinfo("Success", "File loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {e}")

    def generate_schedule(self):
        try:
            if not self.file_path:
                raise ValueError("No file loaded. Please load a file first.")
            
            # Pass all required arguments to the scheduling function
            self.schedule = schedule_employees(
                self.day_numbers, self.day_names, self.skill_mapping, self.shift_data
            )
            messagebox.showinfo("Success", "Schedule generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate schedule: {e}")

    def visualize_schedule(self):
        try:
            if self.schedule is None:
                raise ValueError("No schedule available. Please generate a schedule first.")
            visualize_shifts_needed(self.schedule, self.day_numbers, self.day_names)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize schedule: {e}")

    def visualize_imported_sheet2(self):
        try:
            if self.shift_data is None:
                raise ValueError("No data available. Please load a file first.")

            # Convert shift_data to DataFrame if necessary
            import pandas as pd
            if isinstance(self.shift_data, dict):
                self.shift_data = pd.DataFrame.from_dict(self.shift_data, orient='index')

            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis("off")
            ax.axis("tight")

            table = ax.table(
                cellText=self.shift_data.values,
                rowLabels=self.shift_data.index,
                colLabels=self.shift_data.columns,
                loc="center",
                cellLoc="center",
            )
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.auto_set_column_width(col=list(range(len(self.shift_data.columns))))
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to visualize Sheet2: {e}")

    def save_schedule(self):
        try:
            if self.schedule is None:
                raise ValueError("No schedule available. Please generate a schedule first.")
            save_schedule_to_excel(self.schedule, self.day_numbers, self.day_names)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save schedule: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulingApp(root)
    root.mainloop()