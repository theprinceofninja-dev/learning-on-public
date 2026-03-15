import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


def weighting(
    file_age_hours, file_size_bytes, age_speed=2, size_importance=50
) -> float:
    file_size_mb = file_size_bytes / 1048576

    # How fast importance grows with age
    age_boost = 1 - np.exp(-file_age_hours / age_speed)

    # How much size matters (smaller = better)
    if file_size_mb == 0:
        size_penalty = 1.0
    else:
        size_penalty = np.exp(-file_size_mb / size_importance)

    return age_boost * size_penalty


# Create initial data
ages_hours = np.logspace(-1, 2.3, 100)
sizes_mb = [0.1, 1, 10, 100]

# Create figure and axes
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(bottom=0.3)

# Initial plot
lines = []
for size in sizes_mb:
    weights = [weighting(age, size * 1048576) for age in ages_hours]
    (line,) = ax.plot(ages_hours, weights, label=f"{size} MB", linewidth=2)
    lines.append(line)

ax.set_xscale("log")
ax.set_xlabel("File Age (hours)")
ax.set_ylabel("Importance Score")
ax.set_title("File Importance: Tune with Sliders Below")
ax.legend()
ax.grid(True, alpha=0.3)

# Create sliders
ax_age = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_size = plt.axes([0.2, 0.10, 0.65, 0.03])

slider_age = Slider(ax_age, "Age Speed", 0.5, 10.0, valinit=2.0)
slider_size = Slider(ax_size, "Size Matters", 10.0, 200.0, valinit=50.0)


# Update function
def update(val):
    age_speed = slider_age.val
    size_importance = slider_size.val

    for i, size in enumerate(sizes_mb):
        weights = [
            weighting(age, size * 1048576, age_speed, size_importance)
            for age in ages_hours
        ]
        lines[i].set_ydata(weights)

    fig.canvas.draw_idle()


# Connect sliders
slider_age.on_changed(update)
slider_size.on_changed(update)

plt.show()
