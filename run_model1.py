import time
from SOA import SOA
import model.model1 as m1

if __name__ == '__main__':
    f = m1.Model1()
    soa = SOA(f)
    begin_time = time.time()
    soa.run()
    print("[h, u_p]:", soa.g_best, "C:", m1.C(soa.g_best[0], soa.g_best[1]), "A:", m1.A(soa.g_best[0], soa.g_best[1]))
    print("time cost:", time.time()-begin_time)
