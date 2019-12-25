import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

lambda_4, lambda_3, lambda_2, lambda_1 = 1.231, 1.35, 1.351, 1.23
eta_4, eta_3, eta_2, eta_1 = 1.43, 1.48, 1.459, 1.25

lambd = [lambda_1, lambda_2, lambda_3, lambda_4]
eta = [eta_1, eta_2, eta_3, eta_4]

stand = ['Овал','Круг', 'Овал', 'Диаг. квадрат', '']
fig, ax = plt.subplots()
plt.grid(True)
ax.bar(1 , 1.9, width=0.01, color='white')
ax.bar([i - 0.18 for i in range(1, 5)] , lambd, width=0.3, label='$\\lambda$')
ax.bar([i + 0.18 for i in range(1, 5)], eta, width=0.3, label='$\\frac{1}{\\eta}$')
fig.set_figwidth(12)    #  ширина Figure
fig.set_figheight(6)    #  высота Figure
ax.set_title('Гистограмма коэффициентов вытяжки и обжатия', fontsize=25)
ax.set_xlabel('Форма сечения', fontsize=25)
ax.set_ylabel('Значение коэффициента', fontsize=25)
#ax.set_facecolor('seashell')

for i, cty in enumerate(lambd):
    ax.text(i + 1 - 0.2, cty + 0.1, round(cty, 3), horizontalalignment='center', fontsize=16)

for i, cty in enumerate(eta):
    ax.text(i + 1 + 0.2, cty + 0.1, round(cty, 3), horizontalalignment='center', fontsize=16)


# Title, Label, Ticks and Ylim
#ax.set_title('Bar Chart for Highway Mileage', fontdict={'size':22})
#ax.set(ylabel='Miles Per Gallon', ylim=(0, 30))
plt.xticks(list(range(1, 5)), stand, rotation=0, horizontalalignment='center', fontsize=15)

ax.legend(loc='upper right')

#p1 = patches.Rectangle((.57, -0.005), width=.33, height=.13, alpha=.1, facecolor='green', transform=fig.transFigure)
#p2 = patches.Rectangle((.124, -0.005), width=.446, height=.13, alpha=.1, facecolor='red', transform=fig.transFigure)
#fig.add_artist(p1)
#fig.add_artist(p2)
plt.show()
#with PdfPages('koefficient.pdf') as pdf:
#    plt.savefig('pic/koefficient.pdf')

