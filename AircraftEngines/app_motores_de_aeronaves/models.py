class atmos():
    alt = None
    T0 = None
    P0 = None
    rho0 = None
    a0 = None

    def __init__(self, alt, T0, P0, rho0, a0):
        self.alt = alt
        self.T0 = T0
        self.P0 = P0
        self.rho0 = rho0
        self.a0 = a0  
    
    def __str__(self):
        return self.alt
    
class motor():
    name = None
    motor_type = None
    on_design = None
    ideal = None
    choked = None
    M0 = None
    hpr = None
    cp_c = None
    cp_t = None
    gamma_c = None 
    gamma_t = None
    Tt4 = None
    speed_in_combustion = None
    lenght = None
    
    d0 = None
    d1 = None
    d2 = None
    d3 = None
    d4 = None
    d5 = None
    d6 = None
    d7 = None
    d8 = None
    d9 = None

    def __init__(self, name, motor_type, on_design, ideal, choked, M0, hpr, cp_c, cp_t, gamma_c, gamma_t, Tt4, speed_in_combustion, lenght, d0, d1, d2, d3, d4, d5, d6, d7, d8, d9):
        self.name = name
        self.motor_type = motor_type
        self.on_design = on_design
        self.ideal = ideal
        self.choked = choked
        self.M0 = M0
        self.hpr = hpr
        self.cp_c = cp_c
        self.cp_t = cp_t
        self.gamma_c = gamma_c
        self.gamma_t = gamma_t
        self.Tt4 = Tt4
        self.speed_in_combustion = speed_in_combustion
        self.lenght = lenght
        self.d0 = d0
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7 = d7
        self.d8 = d8
        self.d9 = d9
    
    



    
    