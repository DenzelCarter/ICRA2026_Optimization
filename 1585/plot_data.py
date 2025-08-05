import pandas as pd
import matplotlib.pyplot as plt
import numpy as np # Import numpy for handling potential division by zero

# --- 1. Load Your Data ---
# Make sure this path is correct.
file_path = '1585/Log_2025-08-05_125116.csv'

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    print("Please make sure the script is in the same folder as your CSV file, or provide the full path.")
    exit()

# --- 2. IMPORTANT: Specify Your Column Names ---
# Replace these placeholder names with the actual column headers from your file.
rpm_column = 'Motor Electrical Speed (RPM)'
thrust_column = 'Thrust (N)' # Oldest data used kgf instead
torque_column = 'Torque (N·m)'

# --- 3. Set Analysis Parameters ---
# Set a threshold to filter out unrealistically high Thrust/Torque values.
# Adjust this value based on what you consider a reasonable maximum.
ratio_threshold = 100 # Example: any ratio above 100 will be ignored
rpm_bucket_size = 100 # The size of each RPM bucket for averaging

# --- 4. Calculate and Filter Thrust/Torque Ratio ---
# To avoid errors when torque is zero, we handle the resulting 'inf' values.
with np.errstate(divide='ignore', invalid='ignore'):
    # Calculate the ratio
    thrust_torque_ratio = df[thrust_column] / df[torque_column]
    # Replace infinite values (from division by zero) with NaN
    df['thrust_torque_ratio'] = thrust_torque_ratio.replace([np.inf, -np.inf], np.nan)

# Apply the filter for very large values
df.loc[df['thrust_torque_ratio'] > ratio_threshold, 'thrust_torque_ratio'] = np.nan
print(f"Filtered out Thrust/Torque values greater than {ratio_threshold}")

# --- 5. Bucket Data and Calculate Averages ---
# Create a new column to identify which RPM bucket each row belongs to.
df['rpm_bucket'] = (df[rpm_column] // rpm_bucket_size) * rpm_bucket_size

# Group by the RPM buckets and calculate the mean for each column of interest.
# We use the mean of the RPM column within each bucket for a more accurate x-axis position.
df_agg = df.groupby('rpm_bucket')[[rpm_column, thrust_column, torque_column, 'thrust_torque_ratio']].mean()
print(f"\nData has been averaged into {len(df_agg)} buckets of {rpm_bucket_size} RPM each.")


# --- 6. Create the Plots ---
# Create a figure with three subplots that share the same x-axis (RPM).
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Set a main title for the entire figure
fig.suptitle('Thrust Stand Data Analysis (Averaged)', fontsize=18, y=0.95)

# Plot 1: Thrust vs. RPM (Averaged)
ax1.plot(df_agg[rpm_column], df_agg[thrust_column], marker='o', linestyle='-', color='dodgerblue', label='Thrust')
ax1.set_ylabel('Thrust (N)', fontsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend()
ax1.set_ylim(bottom=-0.01) # Set the negative floor for the y-axis

# Plot 2: Torque vs. RPM (Averaged)
ax2.plot(df_agg[rpm_column], df_agg[torque_column], marker='o', linestyle='-', color='crimson', label='Torque')
ax2.set_ylabel('Torque (N·m)', fontsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend()
ax2.set_ylim(bottom=-0.01) # Set the negative floor for the y-axis

# Plot 3: Thrust/Torque vs. RPM (Averaged)
ax3.plot(df_agg[rpm_column], df_agg['thrust_torque_ratio'], marker='o', linestyle='-', color='green', label='Thrust/Torque')
ax3.set_xlabel('Average RPM per Bucket', fontsize=12)
ax3.set_ylabel('Thrust/Torque (1/m)', fontsize=12)
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.legend()
ax3.set_ylim(bottom=-0.01) # Set the negative floor for the y-axis


# --- 7. Display the Plot ---
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to make room for the suptitle
plt.show()
