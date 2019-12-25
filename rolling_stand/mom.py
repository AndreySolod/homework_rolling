import matplotlib.pyplot as plt
stand = ['Овал','Круг', 'Овал', 'Диаг. квадрат']
fig, ax = plt.subplots()
plt.grid(True)

delta_h = [8.096, 8.253, 10.842, 13.008]
ax.bar(1, 16, width=0.3, color='white')
ax.bar(list(range(1, 5)), delta_h, width=0.3, label='$M$')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
ax.set_title('Гистограмма момента прокатки', fontsize=25)
ax.set_xlabel('Форма сечения', fontsize=25)
ax.set_ylabel('$M$, кН$\cdot$м', fontsize=25)
#ax.set_facecolor('seashell')

for i, cty in enumerate(delta_h):
    ax.text(i + 1, cty + 0.5, round(cty, 3), horizontalalignment='center', fontsize=16)

plt.xticks(list(range(1, 5)), stand, rotation=0, horizontalalignment='center', fontsize=15)

ax.legend(loc='upper right')

plt.show()