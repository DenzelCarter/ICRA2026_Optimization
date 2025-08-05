import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Load Your Data ---
file_path = 'Log_2025-07-31_115621.csv'

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    print("Please make sure the script is in the same folder as your CSV file, or provide the full path.")
    exit()

# --- 2. IMPORTANT: Specify Your Column Names ---
# Replace these placeholder names with the actual column headers from your file.
rpm_column = 'Motor Electrical Speed (RPM)'
thrust_column = 'Thrust (kgf)'
torque_column = 'Torque (N·m)'


# --- 3. Create the Plots ---
# Create a figure with two subplots that share the same x-axis (RPM).
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Plot 1: Thrust vs. RPM
ax1.plot(df[rpm_column], df[thrust_column], marker='o', linestyle='none', color='dodgerblue')
ax1.set_title('Thrust Stand Data', fontsize=16)
ax1.set_ylabel('Thrust (g)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)

# Plot 2: Torque vs. RPM
ax2.plot(df[rpm_column], df[torque_column], marker='o', linestyle='none', color='crimson')
ax2.set_xlabel('RPM', fontsize=12)
ax2.set_ylabel('Torque (N·m)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)


# --- 4. Display the Plot ---
plt.tight_layout()  # Adjusts plot to prevent labels from overlapping
plt.show()