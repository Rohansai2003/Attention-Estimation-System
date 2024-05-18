import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def plot_circle_with_sectors(ang1, ang2,per1, per2, row):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])

    # Sector names and colors
    sector_names = [
        'Disengagement',
        'High Negative',
        'Engagement',
        'Unpleasantness',
        'Low Negative',
        'Pleasantness'
    ]
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']

    # Draw sectors
    for i in range(6):
        wedge = patches.Wedge(center=(0, 0), r=1, theta1=i*60, theta2=(i+1)*60, color=colors[i], alpha=0.3)
        ax.add_patch(wedge)

        # Add sector names
        angle_deg = i * 60 + 30
        angle_rad = np.deg2rad(angle_deg)
        x_text = 1.5 * np.cos(angle_rad)
        y_text = 1.5 * np.sin(angle_rad)
        ax.text(x_text, y_text, sector_names[i],horizontalalignment='center', verticalalignment='center')

    x = 1.2 * np.cos(np.deg2rad(ang1))
    y = 1.2 * np.sin(np.deg2rad(ang1))
    ax.plot([0, x], [0, y], color='blue', linestyle='--', linewidth=1)
    ax.text(x*1.1, y*1.1, f"{int(per1)}%", horizontalalignment='center', verticalalignment='center')
    x = 1.2 * np.cos(np.deg2rad(ang2))
    y = 1.2 * np.sin(np.deg2rad(ang2))
    ax.plot([0, x], [0, y], color='blue', linestyle='--', linewidth=1)
    ax.text(x*1.1, y*1.1, f"{int(per2)}%",horizontalalignment='center', verticalalignment='center')

    plt.axis('off')  # Turn off axis for a cleaner look
    plt.savefig('circle_with_sectors'+str(row)+'.png')
    plt.close()
    return None
