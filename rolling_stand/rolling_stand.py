import sympy

class Stand:
	def __init__(self, r_kat, h_0, h_1, b_0, t_vh, a, v):
		self.r_kat = r_kat
		self.h_0 = h_0
		self.h_1 = h_1
		self.b_0 = b_0
		self.t_vh = t_vh
		self.a = a
		self.v = v
		self.params = {}
		self.is_computing = False
	
	def computing(self):
		if self.is_computing:
			return None
		params{r'\triangle h': self.h_0 - self.h_1}
		params[r'\varepsilon'] = params[r'\triangle h'] / self.h_0
		params[r'l'] = (self.r_kat * params[r'\triangle h']) ** 0.5
		params['u'] = self.v * params[r'\varepsilon'] * 1000 / params[l]
		params[r'\sigma_{\text{ф}}'] = 3250 * sympy.exp(-0.0028 * self.t_vh).n(5) * params[r'\varepsilon'] ** (0.28) * params['u'] ** (0.087)
		def k_2(v):
			if v < 3:
				return 1
			else:
				return 1.53 * v ** (-0.467)
		params[r'\mu_{\text{уст}'] = 0.6 * 0.8 * k_2(self.v) * 1.47 * (1.05 - 0.0005 * self.t)
		params[r'\triangle b'] = 1 / 2 * (l - params[r'\triangle h'] / ( 2 * params[r'\mu_{\text{уст}}'])) * sympy.ln(self.h_0 / self.h_1).n(5)
		params[r'b_{\text{ср}}'] = self.b_0 + params[r'\triangle b'] / 2
		self.b_1 = self.b_0 + params[r'\triangle b']
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
			return (1.155 * (1 + 2 * mu * 0.9 * l / (3 * h_sr * pi.n(5)))) / (gamma * (1 + mu / 3 * l / h_sr))
		def p_sr(h_1, h_0, b_1, b_0, l, mu, sigma_f):
			gm = gamma(b_1, b_0, h_1, h_0, mu)
			n1 = n_1(l, h_1, h_0, mu)
			n2 = n_2(l, h_1, h_0)
			nv = n_v(l, b_1, b_0, h_1, h_0, mu)
			nk = n_k(mu, l, h_1, h_0, gm)
			return gm * n1 * n2 * 1 * nv * nk * sigma_f
		
		p_mid = p_sr(self.h_1, self.h_0, self.b_1, self.b_0, params['l'], params[r'\mu_{\text{уст}}'], params[r'\sigma_{\text{ф}}'])
		params[r'p_{\text{ср}}'] = p_mid
		f_k = p_mid * (self.b_1 + self.b_0) / 2 * params['l']
		params[r'P_{\text{пр}}'] = f_k
		def var_m(mu, l, h_1, h_0):
			h_sr = (h_1 + h_0) / 2
			return mu * l / h_sr

		def var_psi(epsilon, mu, l, h_1, h_0):
			m = var_m(mu, l, h_1, h_0)
			return 1 / (2 - epsilon) * (1 - epsilon * (l ** m / (l ** m - 1) - 1 / m))

		def mom_prok(epsilon, mu, l, h_1, h_0, p):
			psi = var_psi(epsilon, mu, l, h_1, h_0)
			return 2 * p * psi * l / 1000
		
		mp = (params[r'\varepsilon'], params[r'\mu_{\text{уст}}'], params['l'], self.h_1, self.h_0)
		params['M_{\text{пр}}'] = mp
		def delta_t_d(p, h_0, h_1):
			return p * ln(h_0 / h_1).n(5) * 0.8 / (7540 * 548) * 10 ** 6

		def delta_t_v(h_0, h_1, t_vh, l, v):
			return 4.87 / (h_0 + h_1) * (t_vh - 50) * (2 * l * h_0 / (10 ** 3 * (h_0 + h_1) * v)) ** 0.5

		def delta_t_l(t_vh, t_d, t_v, h_1, l_mk, v):
			t = t_vh + t_d - t_v + 273
			return 17.5 * t ** 4 / h_1 * l_mk / v * 10 ** (-15)

		def delta_t_k(t_l):
			return 0.03 * t_l

		def t_vih(t_vh, p, h_0, h_1, v, l, l_mk,):
			t_d = delta_t_d(p, h_0, h_1)
			t_v = delta_t_v(h_0, h_1, t_vh, l, v)
			t_l = delta_t_l(t_vh, t_d, t_v, h_1, l_mk, v)
			t_k = delta_t_k(t_l)
			return t_vh + t_d - t_v - t_l - t_k
		
		params[r'T_{\text{вых}}'] = t_vih(self.t_vh, p_mid, self.h_0, self.h_1, self.v, params['l'], self.a)
		
		self.params = params
	
	def return_params(self):
		if not self.is_computing:
			self.computing()
		return self.params

class CircleStand(Stand):
	def __init__(self, 