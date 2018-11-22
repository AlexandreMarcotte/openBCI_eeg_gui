from time import time, sleep
from random import random, randint
from math import pi
from numpy import sin
import numpy as np
import threading


class CreateSyntheticData(threading.Thread):
    def __init__(self, gv, callback, read_freq=1250):
        super().__init__()
        self.gv = gv
        self.callback = callback
        self.gv.read_period = 1/read_freq
        self.gv.used_read_freq = read_freq
        self.gv.desired_read_freq = read_freq

        self.n_data_created = 0
        # Variable necessary to generate fake signal
        ## time
        self.t = np.linspace(0, 2 * pi, self.gv.DEQUE_LEN)
        ## signal shape
        self.m = 1000
        self.s1 = 3 * self.m * sin(3*self.t)
        self.s2 = self.m * sin(20 * self.t)
        self.s3 = self.m * sin(40 * self.t)
        self.s4 = 10 * self.m * sin(60 * self.t)

        # 100 harmonic signal to test filtering
        self.s = []
        for freq in range(70, 100, 2):
            self.s.append(self.m * sin(freq * self.t))

    def run(self):
        t_init = time()
        """Create random data and a time stamp for each of them"""
        while 1:
            i = self.n_data_created % len(self.t)
            chs_sig = []
            for ch in range(self.gv.N_CH):
                rnd_impulse = randint(0, 100)
                # Set impulse size to be added to the signal once every 100 data
                if rnd_impulse == 0:
                    imp = 5 * self.m
                else:
                    imp = 0
                if ch == 0:
                    signal = self.s1[i] + self.s4[i] #+ random()*self.m + imp
                elif ch == 1:
                    signal = 20 * self.s1[i] + 5
                elif ch == 2:
                    signal = 10 * self.s2[i]
                elif ch == 3:
                    signal = self.s3[i]
                elif ch == 4:
                    signal = self.s4[i]
                elif ch == 5:
                    signal = 0
                    for s in self.s:
                        signal += s[i]
                else:
                    signal = random() * self.m

                chs_sig.append(signal)

            self.callback(chs_sig, time() - t_init, self.n_data_created)
            self.n_data_created += 1

            sleep(self.gv.read_period)