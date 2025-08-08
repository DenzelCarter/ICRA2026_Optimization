import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# --- 1. Specify Your Data File and Column Names ---
file_path = '1585\p_16x5.4 prop 2300 hold.csv'  # <--- SET YOUR FILE PATH HERE

# --- Column Names ---
rpm_column = 'Motor Electrical Speed (RPM)'
thrust_column = 'Thrust (N)'
power_column = 'Electrical Power (W)' # <--- NEW: SPECIFY YOUR POWER COLUMN

# --- Analysis Parameters ---
num_buckets = 12  # Set how many buckets you want to divide the data into
efficiency_threshold = 25 # Sets a max g/W to filter out outliers (e.g. at zero power)
g = 9.80665 # Standard gravity for conversion

# --- 2. Load Data ---
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# --- 3. Clean and Validate Data ---
initial_rows = len(df)
# Remove any rows where thrust or power are negative or zero (to avoid errors).
df = df[(df[thrust_column] >= 0) & (df[power_column] > 0)].copy()
print(f"Removed {initial_rows - len(df)} rows with invalid thrust or power values.")

# --- 4. Calculate Propulsion Efficiency ---
# Efficiency (g/W) = (Thrust in grams) / (Power in Watts)
df['propulsion_efficiency'] = (df[thrust_column] / g * 1000) / df[power_column]
# df['propulsion_efficiency'] = df[thrust_column] / df[power_column]

# Filter out unrealistically high efficiency values
df.loc[df['propulsion_efficiency'] > efficiency_threshold, 'propulsion_efficiency'] = np.nan
print(f"Filtered out propulsion efficiency values greater than {efficiency_threshold} g/W.")

# --- 5. Dynamic Bucketing ---
df['rpm_bucket'] = pd.cut(df[rpm_column], bins=num_buckets)
print(f"Data has been dynamically divided into {num_buckets} RPM buckets.")

# --- 6. Calculate Averages for the Line Plot ---
df_agg = df.groupby('rpm_bucket', observed=True)[[thrust_column, power_column, 'propulsion_efficiency']].mean()
df_agg['rpm_midpoint'] = [bucket.mid for bucket in df_agg.index]

# --- 7. Create the Plots of AVERAGES ---
fig_avg, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig_avg.suptitle('Propulsion System Analysis (Averaged)', fontsize=18, y=0.97)

# Plot 1: Thrust vs. RPM
ax1.plot(df_agg['rpm_midpoint'], df_agg[thrust_column], marker='o', linestyle='-', color='dodgerblue')
ax1.set_ylabel('Mean Thrust (N)')
ax1.grid(True, linestyle='--', alpha=0.6)

# Plot 2: Electrical Power vs. RPM
ax2.plot(df_agg['rpm_midpoint'], df_agg[power_column], marker='o', linestyle='-', color='crimson')
ax2.set_ylabel('Mean Electrical Power (W)')
ax2.grid(True, linestyle='--', alpha=0.6)

# Plot 3: Propulsion Efficiency vs. RPM
ax3.plot(df_agg['rpm_midpoint'], df_agg['propulsion_efficiency'], marker='o', linestyle='-', color='green')
ax3.set_xlabel('RPM Bucket Midpoint')
ax3.set_ylabel('Mean Efficiency (g/W)')
ax3.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- 8. Create Box Plots for Statistical Analysis ---
fig_box, (ax_box1, ax_box2, ax_box3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
fig_box.suptitle('Data Distribution per RPM Bucket', fontsize=18, y=0.97)

# Box Plot 1: Thrust
sns.boxplot(x='rpm_bucket', y=thrust_column, data=df, ax=ax_box1, color='dodgerblue')
ax_box1.set_ylabel('Thrust (N)')
ax_box1.set_xlabel('')

# Box Plot 2: Electrical Power
sns.boxplot(x='rpm_bucket', y=power_column, data=df, ax=ax_box2, color='crimson')
ax_box2.set_ylabel('Electrical Power (W)')
ax_box2.set_xlabel('')

# Box Plot 3: Propulsion Efficiency
sns.boxplot(x='rpm_bucket', y='propulsion_efficiency', data=df, ax=ax_box3, color='green')
ax_box3.set_ylabel('Efficiency (g/W)')
ax_box3.set_xlabel('RPM Bucket')

# Rotate x-axis labels for better readability
for ax in [ax_box1, ax_box2, ax_box3]:
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- 9. Display Both Plots ---
plt.show()