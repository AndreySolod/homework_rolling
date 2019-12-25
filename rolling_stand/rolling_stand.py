import sympy

class Stand:
	def __init__(self, r_kat, h_0, h_1, b_0, t_vh, a, v, lambd, l_0, v_vh_next = None, b_1 = None):
		self.r_kat = r_kat
		self.h_0 = h_0
		self.h_1 = h_1
		self.b_0 = b_0
		self.b_1 = b_1
		self.t_vh = t_vh
		self.a = a
		self.v = v
		self.lambd = lambd
		self.l_0 = l_0
		self.params = {}
		self.v_vh_next = v_vh_next
		self.is_computing = False
	
	def computing(self):
		if self.is_computing:
			return None
		params = dict()
		params[r'$\triangle h$, мм'] = self.h_0 - self.h_1
		params[r'$\varepsilon$'] = params[r'$\triangle h$, мм'] / self.h_0
		params[r'$l$, мм'] = (self.r_kat * params[r'$\triangle h$, мм']) ** 0.5
		params['$u$, $\\frac{1}{c}$'] = self.v * params[r'$\varepsilon$'] * 1000 / params['$l$, мм']
		#params['u'] = 0.105 * n_валков * (params[r'\varepsilon'] * R_рабочий_валков / self.h_0) ** 0.5
		params[r'$\sigma_{\text{ф}}$, МПа'] = 3250 * sympy.exp(-0.0028 * self.t_vh).n(5) * params[r'$\varepsilon$'] ** (0.28) * params['$u$, $\\frac{1}{c}$'] ** (0.087)
		def k_2(v):
			if v < 3:
				return 1
			else:
				return 1.53 * v ** (-0.467)
		params[r'$\mu_{\text{уст}}$'] = 0.6 * 0.8 * k_2(self.v) * 1.47 * (1.05 - 0.0005 * self.t_vh)
		if self.b_1 is None:
			print('b_1 is None!')
			params[r'$\triangle b$'] = 1 / 2 * (l - params[r'$\triangle h$'] / ( 2 * params[r'$\mu_{\text{уст}}$'])) * sympy.ln(self.h_0 / self.h_1).n(5)
		else:
			params[r'$\triangle b$, мм'] = ((self.b_1 - self.b_0) ** 2) ** 0.5
		params[r'$b_{\text{ср}}$, мм'] = self.b_0 + params[r'$\triangle b$, мм'] / 2
		self.b_1 = self.b_0 + params[r'$\triangle b$, мм']
		
		def gamma(b_1, b_0, h_1, h_0, mu):
			if (((b_1 + b_0) / 2) / ((h_0 + h_1) / 2) > 0.465 / mu):
				return 1.155
			else:
				return 1 + mu / 3 * (((b_1 + b_0) / 2) / ((h_0 + h_1) / 2))
		def delta(mu, l, delta_h):
			return (2 * mu * l) / (delta_h)

		def h_n(h_1, h_0, delta):
			return (((1 + (1 + (delta ** 2 - 1) * ((h_0 / h_1) ** delta)) ** 0.5) / (delta + 1)) ** (1 / delta)) * h_1


		def n_1(l, h_1, h_0, mu):
			if l / ((h_1 + h_0) / 2) > 4:
				return 1 + l / (4 * ((h_1 + h_0) / 2))
			elif l / ((h_1 + h_0) / 2) > 2:
				d = delta(mu, l, (h_0 - h_1))
				hn = h_n(h_1, h_0, d)
				return (2 * hn) / ((h_0 - h_1) * (d - 1)) * ((hn / h_1) ** d - 1)
			else:
				return 1 + l / (6 * ((h_1 + h_0) / 2))

		def n_2(l, h_1, h_0):
			if l / ((h_1 + h_0) / 2) > 1:
				return 1
			else:
				return (l / ((h_1 + h_0) / 2)) ** (-0.4)

		def n_v(l, b_1, b_0, h_1, h_0, mu):
			return (1 + ((3 * ((b_1 + b_0) / 2) - l) / (6 * ((b_1 + b_0) / 2))) * mu * l / ((h_1 + h_0) / 2)) / (1 + mu / 2 * l / ((h_0 + h_1) / 2))

		def n_k(mu, l, h_1, h_0, gamma):
			h_sr = (h_1 + h_0) / 2
			return (1.155 * (1 + 2 * mu * 0.9 * l / (3 * h_sr * sympy.pi.n(5)))) / (gamma * (1 + mu / 3 * l / h_sr))
		def p_sr(h_1, h_0, b_1, b_0, l, mu, sigma_f):
			gm = gamma(b_1, b_0, h_1, h_0, mu)
			n1 = n_1(l, h_1, h_0, mu)
			n2 = n_2(l, h_1, h_0)
			nv = n_v(l, b_1, b_0, h_1, h_0, mu)
			nk = n_k(mu, l, h_1, h_0, gm)
			return gm * n1 * n2 * 1 * nv * nk * sigma_f
		
		def k_2(v):
			return 1.53 * v ** (-0.467) if v > 3 else 1

		def mu(v, t):
			return 0.6 * 0.8 * k_2(v) * 1.47 * (1.05 - 0.0005 * t)
		
		p_mid = p_sr(self.h_1, self.h_0, self.b_1, self.b_0, params['$l$, мм'], params[r'$\mu_{\text{уст}}$'], params[r'$\sigma_{\text{ф}}$, МПа'])
		params[r'$p_{\text{ср}}$, МПа'] = p_mid
		f_k = p_mid * (self.b_1 + self.b_0) / 2 * params['$l$, мм'] # Это в ньютонах
		params[r'$P_{\text{пр}}$, кН'] = f_k / 1000 # это в килоньютонах
		def var_m(mu, l, h_1, h_0):
			h_sr = (h_1 + h_0) / 2
			return mu * l / h_sr

		def var_psi(epsilon, mu, l, h_1, h_0):
			m = var_m(mu, l, h_1, h_0)
			if m >= 0.5:
				return 1 / (2 - epsilon) * (1 - epsilon * (l ** m / (l ** m - 1) - 1 / m))
			else:
				return 0.5 * (1 / (1 - epsilon / 2)) * (1 - epsilon * (1 + m) / (2 + m))

		def mom_prok(epsilon, mu, l, h_1, h_0, p):
			psi = var_psi(epsilon, mu, l, h_1, h_0)
			return 2 * p * psi * l / 1000
		
		mp = mom_prok(params[r'$\varepsilon$'], params[r'$\mu_{\text{уст}}$'], params['$l$, мм'], self.h_1, self.h_0, p_mid)
		params['$M_{\\text{пр}}$, кН$\\cdot$мм'] = mp
		
		v_vih = self.v * self.lambd
		#params[r'v_{\text{вых}}'] = v_vih
		params[r'$l_{\text{вых}}$, мм'] = self.l_0 * self.lambd
		
		def delta_t_d(p, h_0, h_1):
			return p * sympy.ln(h_0 / h_1).n(5) * 0.8 / (7900 * 548) * 10 ** 6

		def delta_t_v(h_0, h_1, t_vh, l, v):
			#return 0
			return 4.87 / (h_0 + h_1) * (t_vh - 50) * (2 * l * h_0 / (10 ** 3 * (h_0 + h_1) * v)) ** 0.5

		def delta_t_l(t_vh, t_d, t_v, h_1, l_mk, l_1, v, v_vh_next):
			t = t_vh + t_d - t_v + 273
			tau = l_mk / v + (l_1-l_mk) / v_vh_next # так как моя заготовка > 4 метров
			return 17.5 * t ** 4 / h_1 * tau * 10 ** (-15)

		def delta_t_k(t_l):
			return 0.03 * t_l

		def t_vih(t_vh, p, h_0, h_1, v, l, l_mk, l_1, v_vh_next):
			t_d = delta_t_d(p, h_0, h_1)
			t_v = delta_t_v(h_0, h_1, t_vh, l, v)
			t_l = delta_t_l(t_vh, t_d, t_v, h_1, l_mk, l_1, v, v_vh_next)
			t_k = delta_t_k(t_l)
			return t_vh + t_d - t_v - t_l - t_k, t_d, t_v, t_l, t_k
		
		params[r'$T_{\text{вых}}$, $^{\circ}C$'], t_d, t_v, t_l, t_k = t_vih(self.t_vh, p_mid, self.h_0, self.h_1, self.v, params['$l$, мм'], self.a, params[r'$l_{\text{вых}}$, мм'], self.v_vh_next)
		
		params[r'$\triangle T_{\text{д}}$, $^{\circ}C$'] = t_d
		params[r'$\triangle T_{\text{в}}$, $^{\circ}C$'] = t_v
		params[r'$\triangle T_{\text{л}}$, $^{\circ}C$'] = t_l
		params[r'$\triangle T_{\text{к}}$, $^{\circ}C$'] = t_k
		
		params['$\\tau$'] = self.a / (self.v * 1000) + (params[r'$l_{\text{вых}}$, мм']-self.a) / (self.v_vh_next * 1000)
		
		self.params = params
		self.is_computing = True
	
	def return_params(self):
		if not self.is_computing:
			self.computing()
		return self.params

class LetStripStand(Stand):
	def __init__(self, f_start, f_end, b_start, b_end, d_valkov, t_vh, a, n, lambd, l_0, v_vh_next):
		h_0 = f_start / b_start
		h_1 = f_end / b_end
		d_kat = d_valkov - f_end / b_end
		r_kat = d_kat / 2
		v = (3.1415 * r_kat * 2 * n) / 60_000
		self.v_vh = v / lambd
		#r_kat, h_0, h_1, b_0, t_vh, a, v, lambd, l_0, v_vh_next = None, b_1 = None
		super().__init__(r_kat, h_0, h_1, b_start, t_vh, a, v, lambd, l_0, v_vh_next, b_end)
	
	def computing(self):
		super().computing()
		self.params['$v_{\\text{вх}}$'] = self.v_vh
		self.params['$v_{\\text{вых}}$'] = self.v

class SquareCaliber(LetStripStand):
	def __init__(self, c_1, f_start, b_start, d_valkov, t_vh, a, n, lambd, l_0, v_vh_next):
		self.h_1_sht = (2) ** 0.5 * c_1
		self.r = 0.15 * c_1
		self.h_1 = h_1_sht - 0.83 * self.r
		self.s = 0.025 * c_1
		self.b_pr = self.h_1_sht = self.s
		self.r_1 = 0.125 * self.h_1_sht
		self.perimether = 2 * self.h_1 * 2 ** 0.5
		self.delta = 0.85
		self.area = c_1 ** 2 * (delta * (2 - delta) - 0.43 * (r / c_1) ** 2)
		r_kat = (d_valkov - self.area / self.h_1_sht) / 2
		super().__init__(f_start, b_start, self.area, self.b_pr, r_kat, t_vh, a, n, lambd, l_0, v_vh_next)

class CircleCaliber(LetStripStand):
	def __init__(self, c_1, f_start, b_start, f_end, d_valkov, t_vh, a, n, lambd, l_0, v_vh_next):
		
		if finish:
			c_1 = 1.014 * c_1
		
		def radians(i):
			return i / 360 * 2 * sympy.pi.n(10)
		
		def gamma(c_1):
			if 56 <= c_1 <= 105:
				return 11 + 20 / 60
			elif 50 <= c_1 < 56:
				return 14  + (c_1 - 50) / 6 * (16 + 4 / 6)
			elif 30 <= c_1 < 50:
				return 21 + 50 / 60
			else:
				return 26 + 35 / 60
		
		self.b_k = d / sympy.cos(radians(gamma(c_1))).n(5)
		self.s = 0.025 * c_1
		self.b_vr = self.b_k - self.s * sympy.tan(radians(gamma(c_1)))
		self.r_1 = 0.09 * c_1
		self.perimether = sympy.pi.n(10) * c_1
		self.delta = 0.95
		sela.area = self.b_k ** 2 * (0.785 - 0.667 * (1 - self.delta) * (1 - self.delta ** 2) ** 0.5)
		r_kat = (d_valkov - self.area / self.b_k) / 2
		super().__init__(f_start, self.area, b_start, self.b_k, r_kat, t_vh, a, n, lambd, l_0, v_vh_next)

class EllipseCaliber(LetStripStand):
	def __init__(self, a_k, h_1, f_start, b_start, d_valkov, t_vh, a, n, lambd, l_0, v_vh_next):
		self.b_k = a_k * h_1
		self.h_1 = h_1
		self.R = h_1 * (1 + a_k ** 2) / 4
		self.b_vr = (h_1 - 0.025 * h_1) * (4 * self.R / (h_1 - 0.025 * h_1) - 1) ** 0.5
		self.r_1 = 0.025 * h_1
		self.b_1 = self.b_k - 2 * self.r_1
		self.perimether = 2 * ( h_1 ** 2 + 4 / 3 * self.b_1 ** 2) ** 0.5
		self.area = h_1 ** 2 * (0.6 * (2.07 - 0.85) * (a_k * 0.85 + 0.66 * 0.85 - 0.43))
		r_kat = (d_valkov - self.area / h_1) / 2
		super().__init__(f_start, self.area, b_start, self.b_k, r_kat, t_vh, a, n, lambd, l_0, v_vh_next)

#class CompEllipseCalibre(EllipseCalibre):
#	def __init__(self, 