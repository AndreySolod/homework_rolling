import matplotlib.pyplot as plt
stand = ['Овал','Круг', 'Овал', 'Диаг. квадрат']
fig, ax = plt.subplots()
plt.grid(True)

delta_h = [9.436 , 10.255 , 6.921 , 8.455]
ax.bar(1, 11, width=0.3, color='white')
ax.bar(list(range(1, 5)), delta_h, width=0.3, label='$\\vartriangle h$')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
ax.set_title('Гистограмма абсолютного обжатия', fontsize=25)
ax.set_xlabel('Форма сечения', fontsize=25)
ax.set_ylabel('Значение обжатия $\\vartriangle h$, мм', fontsize=25)
#ax.set_facecolor('seashell')

for i, cty in enumerate(delta_h):
    ax.text(i + 1, cty + 0.7, round(cty, 3), horizontalalignment='center', fontsize=16)

plt.xticks(list(range(1, 5)), stand, rotation=0, horizontalalignment='center', fontsize=15)

ax.legend(loc='upper right')

plt.show()