import matplotlib.pyplot as plt
stand = ['Овал','Круг', 'Овал', 'Диаг. квадрат']
fig, ax = plt.subplots()
plt.grid(True)

delta_h = [0.316, 0.314, 0.309, 0.35]
ax.bar(1, 0.4, width=0.3, color='white')
ax.bar(list(range(1, 5)), delta_h, width=0.3, label='$\\varepsilon$')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
ax.set_title('Гистограмма относительной деформации', fontsize=25)
ax.set_xlabel('Форма сечения', fontsize=25)
ax.set_ylabel('Значение деформации $\\varepsilon$', fontsize=25)
#ax.set_facecolor('seashell')

for i, cty in enumerate(delta_h):
    ax.text(i + 1, cty + 0.03, round(cty, 3), horizontalalignment='center', fontsize=16)

plt.xticks(list(range(1, 5)), stand, rotation=0, horizontalalignment='center', fontsize=15)

ax.legend(loc='upper right')

plt.show()