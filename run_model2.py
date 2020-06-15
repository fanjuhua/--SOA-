import time
from SOA import SOA
import model.model2 as m2

if __name__ == '__main__':
    f = m2.Model2()
    soa = SOA(f)
    begin_time = time.time()
    soa.run()
    print("[h, u_s]:", soa.g_best, "C and A:", m2.get_C_A(soa.g_best[0], soa.g_best[1]))
    print("time cost:", time.time() - begin_time)
