def spring_system():
    import numpy as np
    np.random.seed(7)
    import matplotlib.pyplot as plt
    from matplotlib import animation
    plt.rc('font',size=16)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim([-0.5,5.5])
    ax.set_ylim([-0.5,5.5])
    ax.grid()
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    class system():

        def __init__(self, num_knots=5):
            forbindelser = [[0, 1],
                    [1, 2],
                    [2, 3],
                    [3, 0],
                    [0, 4],
                    [1, 4],
                    [2, 4],
                    [3, 4]]
            
            self.knots = [Knot() for i in range(num_knots)]
                
            self.springs = []
            for indexA,indexB in forbindelser:
                knotA = self.knots[indexA]
                knotB = self.knots[indexB]
                self.springs.append(Spring(knotA,knotB))

        @property
        def total_energy(self):
            return np.sum([spring.energy for spring in self.springs])

        def optimize(self, num_iter=10):
            for i in range (num_iter):
                knot = self.knots[np.random.randint(0,len(self.knots))]
                knot.optimize(self)

        def plot(self):
            for knot in self.knots:
                knot.plot()

            for spring in self.springs:
                spring.plot()

            
            
            


    class Knot():
        def __init__(self):
            self.x = np.random.uniform(0,5)
            self.y = np.random.uniform(0,5)
            self.pos = np.array([self.x, self.y])
            self.plotdisc = ax.plot([self.x], [self.y], "o", markersize=20, zorder=10)[0]


        def plot(self):
            self.plotdisc.set_data([self.x], [self.y])
            return []

        def optimize(self, system):
            delta_x = np.random.normal(0, 0.1)
            delta_y = np.random.normal(0, 0.1)
            
            previous_total_energy = system.total_energy
            
            self.x += delta_x
            self.y += delta_y

            new_total_energy = system.total_energy

            if new_total_energy > previous_total_energy:
                self.x -= delta_x
                self.y -= delta_y
                self.optimize(system)
                
                
                
        
        
    class Spring():
        def __init__(self, knotA, knotB):
            self.k = 1
            self.l0 = 2
            self.knotA = knotA
            self.knotB = knotB
            self.plotspring = ax.plot([self.knotA.x, self.knotB.x], [self.knotA.y, self.knotB.y], "--")[0]

        @property
        def energy(self):
            return 1/2 * self.k * (self.length - self.l0)**2

        @property
        def length(self):
            return np.linalg.norm(self.knotA.pos - self.knotB.pos)

        def plot(self):
            self.plotspring.set_data([self.knotA.x, self.knotB.x], [self.knotA.y, self.knotB.y])
            return []
            



    system1 = system()
    


    
    plt.rc('animation', html='jshtml')

    Nframes = 100

    def update(i):
        system1.optimize()
        system1.plot()
        return []

    anim = animation.FuncAnimation(fig,
                                update,
                                frames=Nframes,
                                interval=50,
                                blit=False)

    
    plt.show()



if __name__ == "__main__":
    spring_system()

