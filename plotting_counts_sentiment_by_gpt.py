import matplotlib.pyplot as plt
#CNN_Biden = [16, 9, 3]
#CNN_Trump = [0, 5, 7]

#BC_Biden = [33,13,1]
#NBC_Trump = [0, 6,1]


#FOX_Biden = [6, 25, 41]
#FOX_Trump = [0, 17, 0]


# Data
organizations = ['CNN', 'NBC', 'FOX']
#Biden_means = [((16 - 3)/28), ((33 - 1) /(47)), ((6 - 41) / (47+25))]
#Trump_means = [((0 - 7) /(12)), ((0 - 1) / (7)), ((0 - 0) / (17))]
Biden_means_BAU = [0, 0, 0]
Trump_means_BAU = [0, 0,-3/17]
# Plotting
plt.figure(figsize=(15, 5))

plt.subplot(1, 2, 1)
plt.bar(organizations, Biden_means_BAU, color='b', alpha=0.7)
plt.title('Sentiment Fraction for Biden Articles on 14th of April, 2024')
plt.ylabel('Mean Sentiment Score')

plt.subplot(1, 2, 2)
plt.bar(organizations, Trump_means_BAU, color='r', alpha=0.7)
plt.title('Sentiment Fraction for Trump Articles on 14th of April, 2024')
plt.ylabel('Mean Sentiment Score')

plt.tight_layout()
plt.show()
