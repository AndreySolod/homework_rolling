spisok = r'''from rolling_stand import Stand, LetStripStand

F_4, F_3, F_2, F_1, F_0 = 922.784, 683.544, 505.872, 411.278, 1134.082
B_4, B_4_sht, B_3, B_2, B_2_sht, B_1, B_0 = 28.282, 45.217, 30.552, 32.738, 20.94, 26.19, 38
D_val, T_0, l_mk, n, = 300, 1020, 4000, 230
lambda_4, lambda_3, lambda_2, lambda_1 = 1.231, 1.35, 1.351,1.23
l_0 = 10_713
#-----------вычисляем скорости прокатки----------------
caliber_4 = LetStripStand(F_0, F_4, B_0, B_4_sht, D_val, T_0, l_mk, n, lambda_4, l_0, 1)
caliber_3 = LetStripStand(F_4, F_3, B_4, B_3, D_val, T_0, l_mk, n, lambda_3, l_0, 1)
caliber_2 = LetStripStand(F_3, F_2, B_3, B_2, D_val, T_0, l_mk, n, lambda_2, l_0, 1)
caliber_1 = LetStripStand(F_2, F_1, B_2_sht, B_1, D_val, T_0, l_mk, n, lambda_1, l_0, 1)
#caliber_4.computing()
#caliber_3.computing()
#caliber_2.computing()
#caliber_1.computing()

#----------вычисляем параметры прокатки----------------------
caliber_4 = LetStripStand(F_0, F_4, B_0, B_4_sht, D_val, T_0, l_mk, n, lambda_4, l_0, caliber_3.v_vh)
caliber_4.computing()
caliber_3 = LetStripStand(F_4, F_3, B_4, B_3, D_val, caliber_4.params[r'$T_{\text{вых}}$, $^{\circ}C$'], l_mk, n, lambda_3, caliber_4.params[r'$l_{\text{вых}}$, мм'], caliber_2.v_vh)
caliber_3.computing()
caliber_2 = LetStripStand(F_3, F_2, B_3, B_2, D_val, caliber_3.params[r'$T_{\text{вых}}$, $^{\circ}C$'], l_mk, n, lambda_2, caliber_3.params[r'$l_{\text{вых}}$, мм'], caliber_1.v_vh)
caliber_2.computing()
caliber_1 = LetStripStand(F_2, F_1, B_2_sht, B_1, D_val, caliber_2.params[r'$T_{\text{вых}}$, $^{\circ}C$'], l_mk, n, lambda_1, caliber_2.params[r'$l_{\text{вых}}$, мм'], caliber_1.v)
caliber_1.computing()

ans = []
for key in caliber_4.params.keys():
	tt = [key, round(caliber_4.params[key], 3), round(caliber_3.params[key], 3), round(caliber_2.params[key], 3), round(caliber_1.params[key], 3)]
	ans.append(tt)

ans = [['Параметр', 'Калибр № 4', 'Калибр № 3', 'Калибр №2', 'Калибр №1']] + ans
for i in ans:
	print(*i, sep=' & ', end='\\\\\n\\hline\n')
	
'''

spisok = spisok.replace('\t', '    ')
spisok = spisok.split('\n')
n = 1

def split_str(string):
	if len(string) < 55:
		return string
	return string[:55] + '\n' + split_str(string[55:]) + '\n'

with open('rs.txt', 'w') as f:
	for i in spisok:
		i = str(n) + '. ' + i
		f.write(split_str(i) + '\n')
		n += 1