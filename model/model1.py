import numpy as np
from model.model import Model
from scipy import integrate

# P_pmk: 轨道桥在kh时刻进行预防性维修的概率
# P_cmk: 轨道桥在[(k-1)h，kh]区间内由于发生故障而进行修复性维修的概率
# C_m: 对轨道桥进行预防性维保的平均费用
# C_M: 对轨道桥进行预防性维修的平均费用
# C_R: 对轨道桥进行修复性维修的平均费用
# T_m: 对轨道桥进行预防性维保的平均停机时间
# T_M: 对轨道桥进行预防性维修的平均停机时间
# T_R: 对轨道桥进行修复性维修的平均停机时间
# EC: 轨道桥寿命周期内的期望费用
# ED: 轨道桥寿命周期内的期望停机时间
# ET: 轨道桥寿命周期的期望长度
# C(T): 轨道桥单位时间费用
# A(T): 轨道桥平均可用度
# T: 一个随机变量，指从轨道桥开始使用到出现必须进行修复的故障时的寿命
# u_p: 轨道桥预防性维修阈值
# u_i: 失效阈值
# h:  预测间隔期
# k: 在(0,t)时间区间内，对轨道桥进行预防性维保、维修的次数
# R(t): t时刻设备可靠度函数
# f(t) = - dR(t) / dt

# P_pmk = 1 - R(k*h+u_p) / R(k*h)
# P_cmk = 1 - R(k*h) / R((k-1)*h)


C_m = 50 # 对轨道桥进行预防性维保的平均费用
C_M = 200 # 对轨道桥进行预防性维修的平均费用
C_R = 1750 # 对轨道桥进行修复性维修的平均费用
T_m = 2 # 对轨道桥进行预防性维保的平均停机时间
T_M = 4 # 对轨道桥进行预防性维修的平均停机时间
T_R = 18 # 对轨道桥进行修复性维修的平均停机时间
A_0 = 0.9

eps = 1e-20
β = 4.39
η = 337.23

N = 100
T = 3070

def changeC_m(x):
    global C_m
    C_m = x

def changeC_M(x):
    global C_M
    C_M = x

def R(t):
    return np.exp(-(t / η) ** β)


def _R(t,k,h):
    return 1 - R(t)/R((k-1)*h)


def P_pmk(k, h, u_p):
    _ = R(k * h + u_p)
    __ = R(k * h)
    if __ == 0 or _/__ == np.nan:
        return 1
    return 1 - _ / __


def P_cmk(k, h):
    _ = R(k * h)
    __ = R((k - 1) * h)
    if __ == 0 or _/__ == np.nan:
        return 1
    return 1 - _ / __


def EC(h, u_p):
    ec = 0
    k = 1
    while k * h <= T:
        ec += ((k - 1) * C_m + C_M) * P_pmk(k, h, u_p) + ((k - 1) * C_m + C_R) * P_cmk(k, h)
        k += 1
    return ec


def ET_f(k, h):
    val2 = R((k-1)*h)
    if val2 < eps:
        val = 0
    else:
        val = integrate.quad(_R,(k-1)*h,k*h,args=(k,h))[0]
    return k * h * P_cmk(k, h) - val


def ET(h, u_p):
    et = 0
    k = 1

    while k * h <= T:
        dt = k * h * P_pmk(k, h, u_p) + ET_f(k, h) * P_cmk(k, h)
        et += dt
        # print(k,dt,P_pmk(k,h,u_0),P_cmk(k,h) )
        # print(k, et)
        k += 1

    return et


def C(h,u_p):
    return EC(h,u_p)/ET(h,u_p)


def ED(h, u_p):
    ed = 0
    k = 1
    while k * h <= T:
        ed += ((k - 1) * T_m + T_M) * P_pmk(k, h, u_p) + ((k - 1) * T_m + T_R) * P_cmk(k, h)
        k += 1
    return ed


def A(h,u_p):
    return 1 - ED(h,u_p)/ET(h,u_p)


class Model1(Model):

    def objective_func(self, x):
        if len(x) != 2:
            raise ValueError("len(x) should be 2 but get", len(x))
        h = x[0]
        u_p = x[1]

        c = C(h,u_p)
        a = A(h,u_p)
        if a < A_0:
            return 10000000-a
        else:
            return c
