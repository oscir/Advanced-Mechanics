def spring_pendulum():
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rc('font',size=16)


    l0 = 3 # ligevægtslængden
    M = 10
    m = 1

    v0 = [1, 0]
    xM0 = 0
    x0 = 0
    y0 = -l0
    vx0 = v0[0]
    vy0 = v0[1]
    vM0 = -vx0 * m/M


    q0 = np.array([xM0, vM0, x0, y0, vx0,vy0])


    g = 9.8
    k = 100

    def dqdt(t, q):
        rM = np.array([q[0],0])
        vM = np.array([q[1]])
        r = np.array(q[2:4])
        v = np.array(q[4:])
        
        rrel = rM -r # en vektor fra m til M
        lt = np.linalg.norm(rrel) # fjederens længde
        rrelhat = rrel / lt # en retningsvektor fra m mod M
        rMhat = np.array([1,0])

        
        
        ffj = k*(lt-l0) * rrelhat #fjederkraften
        aM = -ffj[0]/M # accelerationen på M i x-retningen
        am = (ffj+np.array([0, -g*m]))/m # accelerationen på m
        dqdt = np.concatenate((vM, [aM], v, am)) # alle de tidsafledede sat sammen. Hint: brug np.concatenate
     

        return dqdt




    from scipy.integrate import solve_ivp
    trange = [0, 20]
    t_eval = np.linspace(trange[0], trange[1], 200)
    mysol = solve_ivp(dqdt, trange, q0, max_step=1e-3, t_eval=t_eval)
    ts = mysol.t
    xMs = mysol.y[0]
    xms = mysol.y[2]
    yms = mysol.y[3]

    fig, axes = plt.subplots(1,2,figsize=(10,4))
    C = 0.12
    phi = -np.pi/2

    omega = np.sqrt(1 + m/M)*np.sqrt(g/l0)# formlen fra bogens løsning
    axes[0].plot(ts, np.arctan2(xms-xMs, -yms))
    axes[0].plot(ts, C * np.cos(omega*ts + phi))
    axes[0].set_xlabel(r'$t$')
    axes[0].set_ylabel(r'$\theta$')
    axes[1].plot(ts, xMs)
    axes[1].plot(ts, -(C*m*l0)/(M+m) * np.cos(omega*ts+phi))
    axes[1].set_xlabel(r'$t$')
    axes[1].set_ylabel(r'$x$')


    fig, axes = plt.subplots(1,2,figsize=(10,4))
    C = 0.12
    phi = -np.pi/2

    omega = np.sqrt(1 + m/M)*np.sqrt(g/l0)# formlen fra bogens løsning
    axes[0].plot(ts, np.arctan2(xms-xMs, -yms))
    axes[0].plot(ts, C * np.cos(omega*ts + phi))
    axes[0].set_xlabel(r'$t$')
    axes[0].set_ylabel(r'$\theta$')
    axes[1].plot(ts, xMs)
    axes[1].plot(ts, -(C*m*l0)/(M+m) * np.cos(omega*ts+phi))
    axes[1].set_xlabel(r'$t$')
    axes[1].set_ylabel(r'$x$')


    fig, ax = plt.subplots()

    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    ax.grid("off")
    ax.set_aspect('equal')
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.set_xlim([-2.5, 2.5])
    ax.set_ylim([-3.5, 0.5])

    my_plot = ax.plot([], [], color='C0')[0]
    my_scatter = ax.scatter([], [], s=200, color='C1', zorder=10)
    my_fill = ax.fill([], [], color='C2')[0]

    def update(i):
        my_plot.set_data([xMs[i],xms[i]],[0,yms[i]])
        my_scatter.set_offsets([[xms[i], yms[i]]])
        my_fill.update({'xy': np.array([[-0.5,-0.25],[0.5, -0.25], [0.5, 0.25], [-0.5, 0.25]]) + np.array([xMs[i],0])})
        return []

    fig.tight_layout()


    from matplotlib import animation
    plt.rc('animation', html='jshtml')


    Nframes = len(t_eval)
    anim = animation.FuncAnimation(fig,
                                update,
                                frames=Nframes,
                                interval=30,
                                blit=True)
    plt.show()


if __name__ == "__main__":
    spring_pendulum()