import matplotlib.pyplot as plt
stand = ['Овал','Круг', 'Овал', 'Диаг. квадрат']
fig, ax = plt.subplots()
plt.grid(True)

delta_h = [231.272, 226.629, 244.057, 259.438]
ax.bar(1, 298, width=0.3, color='white')
ax.bar(list(range(1, 5)), delta_h, width=0.3, label='$p_{ср}$')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
ax.set_title('Гистограмма среднего контактного давления', fontsize=25)
ax.set_xlabel('Форма сечения', fontsize=25)
ax.set_ylabel('$p_{ср}$, МПа', fontsize=25)
#ax.set_facecolor('seashell')

for i, cty in enumerate(delta_h):
    ax.text(i + 1, cty + 8, round(cty, 3), horizontalalignment='center', fontsize=16)

plt.xticks(list(range(1, 5)), stand, rotation=0, horizontalalignment='center', fontsize=15)

ax.legend(loc='upper right')

plt.show()