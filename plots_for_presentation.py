import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.legend import Legend

class CustomHandler:
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        width, height = handlebox.width, handlebox.height
        x0, y0 = handlebox.xdescent, handlebox.ydescent

        # Create two patches
        patch1 = Patch(facecolor=orig_handle[0], edgecolor='none',
                       width=width/2, height=height)
        patch2 = Patch(facecolor=orig_handle[1], edgecolor='none',
                       width=width/2, height=height, x=width/2)

        handlebox.add_artist(patch1)
        handlebox.add_artist(patch2)

        return [patch1, patch2]

fig, ax = plt.subplots(figsize=(8, 6))

# Network labels and their corresponding values
news_networks = ['CNN', 'MSNBC', 'FOX']
positive_values = [0.59, 0.21, 0]
second_positive_values = [0.00, 5.46, 0]
negative_values = [0, 0, -2.62]
second_negative_values = [0, 0, -5.78]

# Plotting the bars
ax.bar(news_networks, positive_values, color='blue', width=0.4)
ax.bar(news_networks, second_positive_values, bottom=positive_values, color='lightblue', width=0.4)
ax.bar(news_networks, negative_values, color='red', width=0.4)
ax.bar(news_networks, second_negative_values, bottom=negative_values, color='pink', width=0.4)

ax.set_title('Net Sentiment Surrounding Biden')
ax.set_ylabel('Sentiment Score')
ax.set_ylim(-15, 15)
ax.axhline(0, color='black', linewidth=0.8)

# Creating a custom legend
legend_entries = [(['blue', 'red'], 'Standard Publishing Days'), (['lightblue', 'pink'], 'Trump Bond Trial')]
custom_handles = [([entry[0][0], entry[0][1]], entry[1]) for entry in legend_entries]

ax.legend([handle for handle, label in custom_handles],
          [label for handle, label in custom_handles],
          handler_map={tuple: CustomHandler()},
          handlelength=3, handleheight=2)

plt.tight_layout()
plt.show()

