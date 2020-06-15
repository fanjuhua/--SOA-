import numpy as np
from model.model import Model
from scipy import integrate

eps = 1e-20
# C_o :备件正常订购费用；
# C_e :备件紧急订购费用；
# C_d :因备件未到货导致设备停机造成的经济损失；
# C_u :备件仓储单位时间管理费用；
# C_f :故障预测产生的费用；
# u_s :备件订购阈值；
# L :备件送货时长。
# T :ARMG正常工作时长
# t :ARMG停机时长或备件仓储时长

L = 10
C_o = 4000
C_e = 6000
C_d = 1500
C_u = 400
C_f = 220
A_0 = 0.9
β = 4.39
η = 337.23
T = 3070



def changeC_d(x):
    global C_d
    C_d = x


def changeC_u(x):
    global C_u
    C_u = x

def R(t):
    return np.exp(-(t / η) ** β)


def C_1(k):
    return (k - 1) * C_f + C_e + C_d * t_1()


def P_1(k, h):
    return 1 - R(k * h) / R((k - 1) * h)


def C_2(k, h):
    return k * C_f + C_o + C_d * t_2(k, h)


def P_2(k, h, u_s):
    return (1 - R(k * h + u_s) / R(k * h)) * ((R(k * h) / R((k - 1) * h)) ** k)


def C_3(k, h):
    return k * C_f + C_o + C_u * t_3(k, h)


def P_3(k, h):
    return 1 - P_1(k, h) - P_2(k, h)


def T_1(k, h):
    val = integrate.quad(R, (k - 1) * h, k * h)[0]
    return (k - 1) * h + val


def T_2(k, h):
    val = integrate.quad(R, k * h, k * h + L)[0]
    return k * h + val


def T_3(k, h):
    val= integrate.quad(R, k * h + L, np.inf)[0]
    return k * h + L + val


def t_1():
    return L


def t_2(k, h):
    val = integrate.quad(R, k * h, k * h + L)[0]
    return L - val


def t_3(k, h):
    val = integrate.quad(R, k * h + L, np.inf)[0]
    return val


def ET(h, u_s):
    ans = 0
    for i in range(N):
        k = i + 1
        ans += T_1(k, h) * P_1(k, h) + T_2(k, h) * P_2(k, h, u_s) + T_3(k, h) * P_3(k, h)
    return ans


def EC(h, u_s):
    ans = 0
    for i in range(N):
        k = i + 1
        ans += C_1(k) * P_1(k, h) + C_2(k, h) * P_2(k, h, u_s) + C_3(k, h) * P_3(k, h)
    return ans


def ED(h, u_s):
    ans = 0
    for i in range(N):
        k = i + 1
        ans += t_1() * P_1(k, h) + t_2(k, h) * P_2(k, h, u_s) + t_3(k, h) * P_3(k, h)
    return ans


# def C(h, u_s):
#     return EC(h, u_s) / ET(h, u_s)
#
#
# def A(h, u_s):
#     return ET(h, u_s) / (ET(h, u_s) + ED(h, u_s))


def get_C_A(h, u_s):
    c, a, ec, et, ed = 0, 0, 0, 0, 0
    k = 1
    while k*h <= T:
        r1 = R(k * h)
        r2 = R((k - 1) * h)
        r3 = R(k * h + u_s)
        if r2 < eps:
            p1 = 1
            p2 = 0
        else:
            p1 = 1 - r1 / r2
            p2 = (1 - r3 / r1) * ((r1 / r2) ** k)
        p3 = 1 - p1 - p2

        q = integrate.quad(R, (k - 1) * h, k * h)[0]
        t1 = L
        T1 = (k - 1) * h + q
        c1 = (k - 1) * C_f + C_e + C_d * t1

        q = integrate.quad(R, k * h, k * h + L)[0]
        t2 = L - q
        T2 = k * h + q
        c2 = k * C_f + C_o + C_d * t2

        q = integrate.quad(R, k * h + L, np.inf)[0]
        t3 = q
        T3 = k * h + L + q
        c3 = k * C_f + C_o + C_u * t3

        ec += c1 * p1 + c2 * p2 + c3 * p3
        et += T1 * p1 + T2 * p2 + T3 * p3
        ed += t1 * p1 + t2 * p2 + t3 * p3

        k+=1

    c = ec / et
    a = et / (et + ed)
    return c, a


class Model2(Model):

    def objective_func(self, x):
        if len(x) != 2:
            raise ValueError("len(x) should be 2 but get", len(x))
        h = x[0]
        u_s = x[1]

        C,A = get_C_A(h,u_s)
        if A < A_0:
            return 10000000-A
        else:
            return C

