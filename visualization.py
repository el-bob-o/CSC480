import matplotlib.pyplot as plt
import pandas as pd

def visualize_shifts_needed(shifts_needed, shift_headers):
    try:
        # Convert shifts_needed dictionary to DataFrame for visualization
        shifts_df = pd.DataFrame.from_dict(shifts_needed, orient="index", columns=shift_headers)

        # Plot the DataFrame as a table
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.axis("off")
        ax.axis("tight")

        table = ax.table(
            cellText=shifts_df.values,
            colLabels=shifts_df.columns,
            rowLabels=shifts_df.index,
            cellLoc="center",
            loc="center"
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(shift_headers))))

        plt.show()

    except Exception as e:
        print(f"Failed to visualize Sheet2: {e}")
        raise
