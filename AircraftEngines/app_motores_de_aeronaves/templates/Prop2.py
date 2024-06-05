from ambiance import Atmosphere
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class AircraftEngines:

    def __init__(self, height):
        self.height = height
        self.atm = Atmosphere(height)
        self.T0 = self.atm.temperature[0]
        self.P0 = self.atm.pressure[0]
        self.a0 = self.atm.speed_of_sound[0]
        self.rho0 = self.atm.density[0]
        

    def __str__(self):
        return f"\nDados atmosféricos:\nAltitude = {self.height} m\nT0 = {self.T0} K \nP0 = {self.P0} Pa\na0 = {self.a0} m/s\n"
    
    def get_param(self):
        return self.T0,self.P0,self.a0,self.rho0

    def set_param(self,new_T0:float,new_P0:float,new_a0:float):
        self.height = -1
        self.T0 = new_T0
        self.P0 = new_P0
        self.a0 = new_a0
        
    def printatemperatura(self):
        temperatura_kelvin = self.T0
        temperatura_rankine = temperatura_kelvin * 9/5
        output = {
            'temperatura_kelvin': [],
            'temperatura_Rankine': []
        }
        output['temperatura_kelvin'].append(temperatura_kelvin)
        output['temperatura_Rankine'].append(temperatura_rankine)
        return output

#--------------------------- TURBOJET --------------------------------------------------

    def ideal_turbojet(self, M0, A0, gamma, cp, hpr, Tt4, pi_c):
        """
        Description: This method calculates the on design parameters of an ideal turbojet engine.

        Arguments:
            M0: Mach number                                     [  -  ]
            gamma: Ratio of specific heats                      [kJ/kgK]
            cp: Specific heat at constant pressure              [kJ/kgK]
            hpr: Low heating value of fuel                      [kJ/kg]
            Tt4: Total temperature leaving the burner           [  K  ]
            pi_c: Compressor total pressure ratio               [  -  ]

        Returns: A dictionary containing the list of calculated outputs for each batch.
            pi_c: Compressor total pressure ratio
            F_m0: Specific Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
        """

        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            'm0_dot': [],
            'F': [],
            'FC': [],
            'AF': []            
        }

        R = (gamma - 1)/gamma * cp * 1000  # eq 5.18a
        V0 = self.a0 * M0
        
        tau_r = 1 + (gamma - 1)/2 * M0**2  # eq 5.18c

        tau_c = pi_c**((gamma - 1)/gamma) # assumption ideal cycle
            
        tau_lambda = Tt4/self.T0  # eq 5.18d
        f = cp * self.T0/hpr * (tau_lambda - tau_r * tau_c)  # eq 5.25

        tau_t = 1 - tau_r/tau_lambda * (tau_c - 1)  # eq 5.27
        V9_a0 = (2/(gamma - 1 )* tau_lambda/(tau_r * tau_c) * (tau_r * tau_c * tau_t - 1))**(1/2)  # eq 5.28

        F_m0 = self.a0 * (V9_a0 - M0)  # eq 5.2
        m0_dot = A0*self.rho0*V0
        F = F_m0*m0_dot
        S = f/F_m0  # eq 5.8
        eta_T = 1 - 1/(tau_r * tau_c)  # eq 5.31a
        eta_P = 2 * M0/(V9_a0 + M0)  # eq 5.31b
        eta_Total = eta_P * eta_T # eq 5.31c
        
        FC = F*S
        AF = 1/f

        pi_r = tau_r**(gamma/(gamma-1)) # Gabriel 
        pi_d = pi_b = pi_n = 1 # Gabriel 
        tau_d = tau_n = 1 # Gabriel 
        tau_b = tau_lambda/(tau_r*tau_d*tau_c) # Gabriel 
        pi_t = tau_t**(gamma/(gamma-1)) # Gabriel 
        P0_P9 = 1 # Gabriel 
        Pt9_P9 = pi_r*pi_c*pi_t # Gabriel 
        Tt9 = self.T0*tau_r*tau_c*tau_b*tau_t # Gabriel 
        T9_T0 = tau_b # Gabriel 
        T9_Tt9 = T9_T0*self.T0/Tt9 # Gabriel 
        M9 = (2/(gamma-1)*(tau_r*tau_c*tau_t))**0.5 # Gabriel 

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output,tau_lambda, pi_r, tau_r, pi_d, tau_d, pi_c, tau_c, pi_b, tau_b, pi_t, tau_t, pi_n, tau_n, P0_P9, Pt9_P9, T9_Tt9, T9_T0, M9
              
    def real_turbojet(self, M0, A0, gamma_c, gamma_t, cp_c, cp_t, hpr, Tt4 , pi_c, pi_d_max, pi_b, pi_n, e_c, e_t, eta_b, eta_m, P0_P9):
        """
        Description: This method calculates the on design parameters of an non ideal turbojet engine.

        Arguments:
            M0: Mach number
            gamma_c: Ratio of specific heats in the compressor          [  -  ]
            gamma_t: Ratio of specific heats in the turbine             [  -  ]
            cp_c: Specific heat at constant pressure in the compressor  [kJ/kgK]
            cp_t: Specific heat at constant pressure in the turbine     [kJ/kgK]
            hpr: Low heating value of fuel                              [kJ/kg]
            Tt4: Total temperature leaving the burner                   [  K  ]
            pi_c: Compressor total pressure ratio                       [  -  ]
            pi_d_max: Difuser maximum total pressure ratio              [  -  ]
            pi_b: Burner total pressure ratio                           [  -  ]
            pi_n: Nozzle total pressure ratio                           [  -  ]
            e_t: Polytropic compressor efficiency                       [  -  ]
            e_t: Polytropic turbine efficiency                          [  -  ]
            eta_b: Combustor efficiency                                 [  -  ]
            eta_m: Mechanical efficiency                                [  -  ]
            P0_P9: Ratio between Po/P9                                  [  -  ]

        Returns: A dictionary containing the list of calculated outputs for each batch.
            pi_c: Compressor total pressure ratio
            F_m0: Specific Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
        """

        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            'm0_dot': [],
            'F': [],
            'FC': [],
            'AF': []  
        }

        # Gas constants
        R_c    = ((gamma_c - 1)/gamma_c ) * (cp_c) * 1000
        R_t    = ((gamma_t - 1)/gamma_t ) * (cp_t) * 1000

        # Free stream
        a0    = (gamma_c*R_c*self.T0)**0.5
        V0    = a0 * M0
        m0_dot = A0*self.rho0*V0

        # Free flow parameters
        tau_r    = 1 + ((gamma_c - 1)/2 ) * (M0**2)
        pi_r     = tau_r**(gamma_c/(gamma_c - 1))
        
        if (M0 <= 1):
            eta_r  = 1
        elif (M0 > 1 and M0 <= 5):
            eta_r  = 1 - 0.075*((M0 - 1)**(1.35))
        elif (M0 > 5):
            eta_r  = 800/(M0**4 + 935)

        # Diffuser
        pi_d   = pi_d_max*eta_r
        tau_d = pi_d**((gamma_c-1)/gamma_c)
        
        # Compressor
        tau_c    = (pi_c)**((gamma_c - 1)/(gamma_c*e_c))
        eta_c    = (pi_c**((gamma_c - 1)/gamma_c) - 1)/(tau_c - 1)

        # Burner
        tau_lambda    = cp_t*Tt4/(cp_c*self.T0)
        f             = (tau_lambda-tau_r*tau_c)/( (hpr*eta_b/(cp_c*self.T0)) - tau_lambda)
        tau_b = Tt4/(self.T0*tau_d*tau_r*tau_c)
        
        # Turbine
        tau_t  = 1 - (1/(eta_m*(1+f)))*(tau_r/tau_lambda)*(tau_c-1)
        pi_t   = tau_t**(gamma_t/((gamma_t-1)*e_t))
        eta_t  = (1 - tau_t)/(1 - tau_t**(1/e_t))
        
        tau_n = 1

        # Auxiliar
        Pt9_P9 = (P0_P9)*pi_r*pi_d*pi_c*pi_b*pi_t*pi_n
        Tt9_T0 = tau_r*tau_d*tau_c*tau_b*tau_t*tau_n 
        M9     = (2/(gamma_t - 1)*(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
        T9_T0  = (tau_lambda*tau_t)/( ((Pt9_P9)**((gamma_t-1)/gamma_t)))*(cp_c/cp_t)
        V9_a0  = M9*( ( gamma_t*R_t*(T9_T0)/(gamma_c*R_c) )**0.5 )
        
        T9  = self.T0*T9_T0
        #Tt9 = self.T0*T9_T0 #? Isso não faz sentido - Gabriel
        Tt9 = tau_r*tau_d*tau_c*tau_b*tau_t*tau_n*self.T0 # Gabriel
        T9_Tt9 = T9/Tt9 # Gabriel


        # Results
        F_m0      = a0*((1+f)*V9_a0 - M0 + (1+f)*R_t*T9_T0/(R_c*V9_a0)*(1-P0_P9)/gamma_c)
        F         = F_m0*m0_dot
        S         = f/F_m0
        eta_T     = ((a0**2)*( (1+f)*V9_a0**2 - M0**2 )/(2*f*(hpr*1000)))
        eta_P     = ( 2*V0*F_m0/( (a0**2)*( (1+f)*V9_a0**2 - M0**2 ) ) )
        eta_Total = eta_T*eta_P
        
        FC = F*S
        AF = 1/f

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        
        return output,tau_lambda, pi_r, tau_r, pi_d, tau_d, pi_c, tau_c, pi_b, tau_b, pi_t, tau_t, pi_n, tau_n, P0_P9, Pt9_P9, T9_Tt9, T9_T0, M9

    def offdesign_turbojet(self,
        M0,
        A0,
        Tt4,
        P0_P9,

        # Constantes
        gamma_c,
        cp_c,
        gamma_t,
        cp_t,
        hpr,
        pi_d_max,
        pi_b,
        pi_t,
        pi_n,
        tau_t,
        eta_c,
        eta_b,
        eta_m,

        # Condições de referência
        M0_R,
        T0_R,
        P0_R,
        tau_r_R,
        pi_r_R,
        Tt4_R,
        pi_d_R,
        pi_c_R,
        tau_c_R,
        Pt9_P9_R,

        #  Inputs extras do Rolls-Royce Nene
        m0_R = 50 # kg/s (?)
        ):

        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'F': [],
            'S': [],
            'FC':[],
            'AF':[],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            'm0_dot':[]
        }

        T0 = self.T0
        P0 = self.P0

        Tt2_R = T0_R*tau_r_R

        #  Equations
        R_c = (gamma_c - 1)/gamma_c*cp_c * 1000 # J/(kg.K)
        R_t = (gamma_t - 1)/gamma_t*cp_t * 1000 # J/(kg.K)
        
        a0 = (gamma_c*R_c*T0)**(1/2) # m/s
        V0 = a0*M0
        
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35

        pi_d = pi_d_max*eta_r
        tau_d = pi_d**((gamma_c-1)/gamma_c)
        
        Tt2 = T0*tau_r
        
        tau_c = 1 + (tau_c_R - 1)*Tt4/Tt2/(Tt4_R/Tt2_R)
        pi_c = (1 + eta_c*(tau_c - 1))**(gamma_c/(gamma_c - 1))
        
        tau_lambda = cp_t*Tt4/(cp_c*T0)
        tau_b = Tt4/(self.T0*tau_d*tau_r*tau_c)

        
        tau_n = 1
        
        f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*T0) - tau_lambda) # kgFuel/kgAir
        m0_dot = m0_R*P0*pi_r*pi_d*pi_c/(P0_R*pi_r_R*pi_d_R*pi_c_R)*(Tt4_R/Tt4)**(1/2) # kg/s
        Pt9_P9 = P0_P9*pi_r*pi_d*pi_c*pi_b*pi_t*pi_n
        M9 = (2/(gamma_t - 1)*(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
        T9_T0 = (tau_lambda*tau_t)/((Pt9_P9)**((gamma_t - 1)/gamma_t))*(cp_c/cp_t)
        Tt9_T0 = tau_r*tau_d*tau_c*tau_b*tau_t*tau_n
        V9_a0 = M9*(gamma_t*R_t/(gamma_c*R_c)*T9_T0)**(1/2)
        F_m0 = a0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t*T9_T0/(R_c*V9_a0)*(1 - P0_P9)/gamma_c) # N/(kg/s)
        F = F_m0*m0_dot # N
        S = f/F_m0 # (kgFuel/s)/N
        
        eta_T = a0**2*((1 + f)*V9_a0**2 - M0**2)/(2*f*hpr*1000)
        eta_P = 2*V0*F_m0/(a0**2*((1 + f)*V9_a0**2 - M0**2))
        eta_Total = eta_P*eta_T
        
        N_NR = (T0*tau_r/(T0_R*tau_r_R)*(pi_c**((gamma_c - 1)/gamma_c) - 1)/(pi_c_R**((gamma_c - 1)/gamma_c) - 1))**(1/2)
        A9_A9R = (Pt9_P9/Pt9_P9_R)**((gamma_t + 1)/(2*gamma_t))*((Pt9_P9_R**((gamma_t - 1)/gamma_t) - 1)/(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
        mc2_mc2_R = pi_c/pi_c_R*((Tt4_R/Tt2_R)/(Tt4/Tt2))**(1/2) # vazão mássica corrigida no compressor

        #  Outputs extras
        V9 = V9_a0*a0 # m/s
        AF = 1/f  # kgAir/kgFuel
        
        Pt4 = P0*pi_r*pi_d*pi_c*pi_b # Pa
        Pt9 = P0*pi_r*pi_d*pi_c*pi_b*pi_t # Pa
        
        T9 = T0*T9_T0 # K
        #Tt9 = self.T0*T9_T0 #Não faz sentido - Gabriel
        Tt9 = tau_r*tau_d*tau_c*tau_b*tau_t*tau_n*T0 #Gabriel
        T9_Tt9 = T9/Tt9 #Gabriel

        #m0_dot = A0*self.rho0*V0 #já está sendo calculado acima - Gabriel
        F  = F_m0*m0_dot
        FC = F*S
        AF = 1/f

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output,tau_lambda, pi_r, tau_r, pi_d, tau_d, pi_c, tau_c, pi_b, tau_b, pi_t, tau_t, pi_n, tau_n, P0_P9, Pt9_P9, T9_Tt9, T9_T0, M9, N_NR

#------------------------------- TURBOFAN ------------------------------------------------------------
    # NOT BEING USED.
    def ideal_turbofan(self, M0, gamma, cp, hpr, Tt4, pi_c, pi_f, alpha, batch_size=1, min_pi_c=0.001, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an ideal turbofan engine.

        Arguments:
            M0: Mach number                                             [  -  ]
            gamma: Ratio of specific heats                              [  -  ]
            cp: Specific heat at constant pressure                      [kJ/kgK]
            hpr: Low heating value of fuel                              [kJ/kg]
            Tt4: Total temperature leaving the burner                   [  K  ]
            pi_c: Compressor total pressure ratio                       [  -  ]
            batch_size: Number of points to iterate pi_c                [  -  ]
            min_pi_c: Min value for pi_c (only used in batch)           [  -  ]
            max_pi_c: Max value for pi_c (only used in batch)           [  -  ]

        Returns: A dictionary containing the list of calculated outputs for each batch.
            pi_c: Compressor total pressure ratio
            F_m0: Specific Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
            FR: Thrust ratio
        """
        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            'FR': []
        }

        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c)/batch_size

        while pi_c <= max_pi_c:

            R = (gamma - 1)/gamma * cp # eq padrão
            V0 = self.a0 * M0 # eq padrão
            tau_r = 1 + (gamma - 1)/2 * M0**2 # eq 5.18c
            pi_r = tau_r ** (gamma / (gamma - 1))
            tau_f = pi_f**((gamma - 1)/gamma) # eq 5.58f
            V19_a0 = (2/(gamma - 1) * (tau_r * tau_f - 1))**(1/2) # eq 5.58h
            tau_c = pi_c**((gamma - 1)/gamma)  # assumption ideal cycle # eq 5.58e
            tau_lambda = Tt4/self.T0 # eq 5.58d
            f = cp * self.T0/hpr * (tau_lambda - tau_r * tau_c) # eq 5.58j
            tau_t = 1 - tau_r/tau_lambda * (tau_c - 1 + alpha * (tau_f - 1)) # eq 5.52
            pi_t = tau_t ** (gamma / (gamma - 1)) 
            V9_a0 = (2/(gamma - 1) * (tau_lambda - tau_r*(tau_c - 1 + alpha * (tau_f - 1)) - tau_lambda/(tau_r * tau_c)))**(1/2)  #eq 5.53
            F_m0 = self.a0 * 1/(1 + alpha) * (V9_a0 - M0 + alpha * (V19_a0 - M0)) # eq. 5.48 (por que não entra o g_c)
            f = cp * self.T0/hpr * (tau_lambda - tau_r * tau_c) # eq 5.51
            S = f/((1 + alpha) * F_m0) #eq 5.54
            eta_T = 1 - 1/(tau_r * tau_c) # eq 5.22
            eta_P = 2 * M0 * (V9_a0 - M0 + alpha * (V19_a0 - M0))/((V9_a0 * self.a0)**2/(self.a0**2) - M0**2 + alpha * ((V19_a0*self.a0)**2/(self.a0**2) - M0**2)) # eq 5.55
            eta_Total = eta_P * eta_T # eq 5.58n
            FR = (V9_a0 - M0)/(V19_a0 - M0)  #eq 5.57
            
            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)
            output['FR'].append(FR)

            pi_c += pi_c_increase
        pi_c -= pi_c_increase
        return output,tau_r,pi_r,tau_f,tau_c,tau_lambda,tau_t,pi_t

    def real_turbofan(self,M0,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4,pi_d_max,pi_b,pi_n,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_b,eta_mL,eta_mH,P0_P9,P0_P19,tau_n,tau_fn,pi_cL,pi_cH,pi_f,alpha,A0):

        """
        Description: This method calculates the on design parameters of a real twin spool turbofan engine.

        Arguments:
            M0: Mach number
            gamma_c: Ratio of specific heats at the compressor
            gamma_t: Ratio of specific heats at the turbine
            cp_c: Specific heat at constant pressure at the compressor
            cp_t: Specific heat at constant pressure at the turbine
            hpr: Low heating value of fuel
            Tt4: Total temperature leaving the burner
            pi_d_max: Maximum total pressure ratio at the difuser
            pi_b: Total pressure ratio at the burner
            pi_n: Total pressure ratio at the nozzle
            pi_fn: Total pressure ratio between the fan and the nozzle
            e_cL: Politropic efficiency of the low pressure compressor
            e_cH: : Politropic efficiency of the high pressure compressor
            e_f: Politropic efficiency of the fan
            e_tL: Politropic efficiency of the low pressure turbine
            e_tH: Politropic efficiency of the high pressure turbine
            eta_b: Burner efficiency
            eta_mL: Mechanical efficiency for low pressure
            eta_mH: Mechanical efficiency for high pressure
            P0_P9: Pressure ratio between the freestream and the gas generator outlet
            P0_P19: Pressure ratio between the freestream and the fan outlet
            tau_n: Total temperature ratio at the nozzle
            tau_fn: Total temperature ratio between the fan and the nozzle
            pi_cL: Total pressure ratio at the low pressure compressor
            pi_cH: Total pressure ratio at the high pressure compressor
            pi_f: Total pressure ratio at the fan
            alpha: Bypass ratio

        Returns: A dictionary containing the list of calculated outputs for each batch.
            F_m0: Specific Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
            FR: Thrust ratio
        """
        output = {
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            'FR': [],
            'm0_dot': [],
            'F': [],
            'AF': [],
            'FC': []            
        }

        R_c = (gamma_c - 1) / gamma_c * cp_c * 1000  # eq. 7.52a
        R_t = (gamma_t - 1) / gamma_t * cp_t * 1000  # eq. 7.52b
        a0 = (gamma_c * R_c * self.T0) ** (1 / 2)  # eq. 7.52c 
        V0 = a0 * M0  # eq. 7.52d

        # Free stream parameters
        tau_r = 1 + (gamma_c - 1) / 2 * M0 ** 2  # eq. 7.52e
        pi_r = tau_r ** (gamma_c / (gamma_c - 1))  # eq. 7.52f

        if M0 <= 1:
            eta_r = 1  # eq. 7.52g
        else:
            eta_r = 1 - 0.075 * (M0 - 1) ** 1.35  # eq. 7.52h

        # Diffuser parameters
        pi_d = pi_d_max * eta_r  # eq. 7.52i
        tau_d = pi_d ** ((gamma_c - 1) / gamma_c)   # eq. padrão

        # Fan parameters
        tau_f = pi_f ** ((gamma_c - 1) / (gamma_c * e_f))  # eq. 7.52m
        eta_f = (pi_f ** ((gamma_c - 1) / gamma_c) - 1) / (tau_f - 1)  # eq. 7.52n

        # Enthalpy
        tau_lambda = cp_t * Tt4 / (cp_c * self.T0)  # eq. 7.52j

        # Compressor parameters
        tau_cL = pi_cL ** ((gamma_c - 1) / (gamma_c * e_cL))
        tau_cH = pi_cH ** ((gamma_c - 1) / (gamma_c * e_cH))
        eta_cL = (pi_cL ** ((gamma_c - 1) / gamma_c) - 1) / (tau_cL - 1)
        eta_cH = (pi_cH ** ((gamma_c - 1) / gamma_c) - 1) / (tau_cH - 1)

        # Turbine parameters
        f = (tau_lambda - tau_r * tau_d * tau_f * tau_cL * tau_cH) / (hpr * eta_b / (cp_c * self.T0) - tau_lambda)
        tau_tH = 1 - (tau_cH - 1) / (1 + f) / tau_lambda * tau_r * tau_d * tau_f * tau_cL * eta_mH
        tau_tL = 1 - ((alpha * (tau_f - 1) + (tau_cL - 1)) * eta_mL / (1 + f) * tau_r * tau_d / tau_lambda / tau_tH)
        pi_tH = tau_tH ** (gamma_t / ((gamma_t - 1) * e_tH))
        pi_tL = tau_tL ** (gamma_t / ((gamma_t - 1) * e_tL))
        eta_tH = (tau_tH - 1) / (pi_tH ** ((gamma_t - 1) / gamma_t) - 1)
        eta_tL = (tau_tL - 1) / (pi_tL ** ((gamma_t - 1) / gamma_t) - 1)

        # Engine core parameters
        Pt9_P9 = P0_P9 * pi_r * pi_d * pi_f * pi_cL * pi_cH * pi_b * pi_tH * pi_tL * pi_n
        M9 = (2 / (gamma_c - 1) * (Pt9_P9 ** ((gamma_c - 1) / gamma_c) - 1)) ** (1 / 2)
        Tt9_T0 = cp_c / cp_t * tau_lambda * tau_tH * tau_tL * tau_n
        T9_T0 = Tt9_T0 / Pt9_P9 ** ((gamma_t - 1) / gamma_t)
        T9_Tt9 = T9_T0/Tt9_T0
        V9_a0 = M9 * (R_t * gamma_t / (R_c * gamma_c) * T9_T0) ** (1 / 2)
        tau_b = Tt9_T0/(tau_r*tau_d*tau_cH*tau_cL*tau_tH*tau_tL*tau_n)

        # Parametros referentes a saida do bypass apos o fan
        Pt19_P19 = P0_P19 * pi_r * pi_d * pi_f * pi_fn
        M19 = (2 / (gamma_c - 1) * (Pt19_P19 ** ((gamma_c - 1) / gamma_c) - 1)) ** (1 / 2)
        Tt19_T0 = tau_r * tau_d * tau_f * tau_fn
        T19_T0 = Tt19_T0 / Pt19_P19 ** ((gamma_c - 1) / gamma_c)
        V19_a0 = M19 * (T19_T0) ** (1 / 2)

        # Engine performance parameters
        FF_m0 = alpha / (1 + alpha) * a0 * (V19_a0 - M0 + T19_T0 / V19_a0 * (1 - P0_P19) / gamma_c)  # N/(kg/s)
        FC_m0 = 1 / (1 + alpha) * a0 * ((1 + f) * V9_a0 - M0 + (1 + f) * R_t / R_c * T9_T0 / V9_a0 * (1 - P0_P9) / gamma_c)  # N/(kg/s)
        F_m0 = FF_m0 + FC_m0  # N/(kg/s)
        S = f / ((1 + alpha) * F_m0)
        FR = FF_m0 / FC_m0
        eta_T = a0 * a0 * ((1 + f) * V9_a0 * V9_a0 + alpha * (V19_a0 * V19_a0) - (1 + alpha) * M0 * M0) / (2 * f * hpr * 1000) # creio que faltava um * 1000 aqui para adequar ao SI
        eta_P = 2 * M0 * ((1 + f) * V9_a0 + alpha * V19_a0 - (1 + alpha) * M0) / ( (1 + f) * (V9_a0 ** 2) + alpha * V19_a0 ** 2 - (1 + alpha) * M0 ** 2)
        eta_Total = eta_P * eta_T

        m0_dot = self.rho0*V0*A0 # Gabriel
        F = F_m0*m0_dot # Gabriel
        AF = 1/f # Gabriel
        FC = F*S # Gabriel

        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        output['FR'].append(FR)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['AF'].append(AF)
        output['FC'].append(FC)

        return output,self.T0,tau_r,pi_r,pi_d,tau_d,tau_f,tau_lambda,tau_cL,tau_cH,tau_tH,tau_tL,pi_tH,pi_tL,Pt9_P9,Tt9_T0,T9_T0,Pt19_P19,Tt19_T0,T19_T0,T9_Tt9,tau_b

    def real_turbofan_off_design(self,M0,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4,pi_d_max,pi_b,pi_c,pi_tH,pi_n,pi_fn,tau_tH,eta_f,eta_cL,eta_cH,eta_b,eta_mL,eta_mH,eta_tL,M0_R,T0_R,P0_R,
        tau_r_R,tau_lambda_R,pi_r_R,Tt4_R,pi_d_R,pi_f_R,pi_cH_R,pi_cL_R,pi_tL_R,tau_f_R,tau_tL_R,alpha_R,M9_R,M19_R,m0_R,tau_n):

        tau_cH_R = pi_cH_R**((gamma_c - 1)/(gamma_c))
        tau_cL_R = pi_cL_R**((gamma_c - 1)/(gamma_c))
        R_c = (gamma_c - 1)/gamma_c*cp_c * 1000
        R_t = (gamma_t - 1)/gamma_t*cp_t * 1000
        a0 = (gamma_c*R_c*self.T0)**(1/2) 
        V0 = a0*M0
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))

        

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35


        pi_d = pi_d_max*eta_r
        tau_d = pi_d ** ((gamma_c - 1) / gamma_c)

        tau_lambda = cp_t*Tt4/(cp_c*self.T0)

        teste = 10
        while teste > 0.0001:
            tau_tL = tau_tL_R
            tau_f = tau_f_R
            tau_cL = tau_cL_R
            pi_tL = pi_tL_R
            pi_cL = pi_cL_R
            tau_cH = 1 + Tt4/self.T0/(Tt4_R/T0_R)*(tau_f_R*tau_cL_R)/(tau_r*tau_cL)*(tau_cH_R - 1)
            pi_cH = (1 + eta_cH*(tau_cH - 1))**(gamma_c/(gamma_c - 1))
            pi_f = (1 + (tau_f - 1)*eta_f)**(gamma_c/(gamma_c - 1))
            Pt19_P0 = pi_r*pi_d*pi_f*pi_fn
            if Pt19_P0 < ((gamma_c + 1)/2)**(gamma_c/(gamma_c - 1)):
                Pt19_P19 = Pt19_P0
            else:
                Pt19_P19 = ((gamma_c + 1)/2)**(gamma_c/(gamma_c - 1))
            M19 = (2/(gamma_c - 1)*(Pt19_P19**((gamma_c - 1)/gamma_c) - 1))**(1/2)
            Pt9_P0 = pi_r*pi_d*pi_f*pi_cL*pi_cH*pi_b*pi_tH*pi_tL*pi_n
            if Pt9_P0 < ((gamma_t + 1)/2)**(gamma_t/(gamma_t - 1)):
                Pt9_P9 = Pt9_P0
            else:
                Pt9_P9 = ((gamma_t + 1)/2)**(gamma_t/(gamma_t - 1))

            M9 = (2/(gamma_t - 1)*(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
            MFP_M19 = M19*(gamma_c/R_c)**(1/2)*(1 + (gamma_c - 1)/2*M19**2)**((gamma_c + 1)/(2*(1 - gamma_c)))
            MFP_M19_R = M19_R*(gamma_c/R_c)**(1/2)*(1 + (gamma_c - 1)/2*M19_R**2)**((gamma_c + 1)/(2*(1 - gamma_c)))
            alpha = alpha_R*pi_cL_R*pi_cH_R/pi_f_R/(pi_cL*pi_cH/pi_f)*((tau_lambda)/(tau_r*tau_f)/(tau_lambda_R/(tau_r_R*tau_f_R)))**(1/2)*MFP_M19/MFP_M19_R
            tau_f = 1 + (tau_f_R - 1)*((1 - tau_tL)/(1 - tau_tL_R)*(tau_lambda/tau_r)/(tau_lambda_R/tau_r_R)*(tau_cL_R - 1 + alpha_R*(tau_f_R - 1))/(tau_cL_R - 1 + alpha*(tau_f_R - 1)))
            tau_cL = 1 + (tau_f - 1)*(tau_cL_R - 1)/(tau_f_R - 1)
            pi_cL = (1 + eta_cL*(tau_cL - 1))**(gamma_c/(gamma_c - 1))
            tau_tL = 1 - eta_tL*(1 - pi_tL**((gamma_t - 1)/gamma_t))
            MFP_M9 = M9*(gamma_t/R_t)**(1/2)*(1 + (gamma_t - 1)/2*M9**2)**((gamma_t + 1)/(2*(1 - gamma_t)))
            MFP_M9_R = M9_R*(gamma_t/R_t)**(1/2)*(1 + (gamma_t - 1)/2*M9_R**2)**((gamma_t + 1)/(2*(1 - gamma_t)))
            pi_tL = pi_tL_R*(tau_tL/tau_tL_R)**(1/2)*MFP_M9_R/MFP_M9
            teste = abs(tau_tL - tau_tL_R)
            tau_tL_R = tau_tL
            tau_f_R = tau_f
            tau_cL_R = tau_cL
            pi_tL_R = pi_tL

        m0 = m0_R*(1 + alpha)/(1 + alpha_R)*self.P0*pi_r*pi_d*pi_cL*pi_cH/(P0_R*pi_r_R*pi_d_R*pi_cL_R*pi_cH_R)*(Tt4_R/Tt4)**(1/2)
        f = (tau_lambda - tau_r*tau_cL*tau_cH)/(hpr*eta_b/(cp_c*self.T0) - tau_lambda)
        Tt9_T0 = cp_c / cp_t * tau_lambda * tau_tH * tau_tL * tau_n
        T9_T0 = tau_lambda*tau_tH*tau_tL/(Pt9_P9**((gamma_t - 1)/gamma_t))*cp_c/cp_t
        T9_Tt9 = T9_T0/Tt9_T0
        V9_a0 = M9*(gamma_t*R_t/(gamma_c*R_c)*T9_T0)**(1/2)
        T19_T0 = tau_r*tau_f/(Pt19_P19**((gamma_c - 1)/gamma_c))
        V19_a0 = M19*(T19_T0)**(1/2)
        P19_P0 = Pt19_P0/(1 + (gamma_t - 1)/2*M19**2)**(gamma_t/(gamma_t - 1))
        P9_P0 = Pt9_P0/(1 + (gamma_c - 1)/2*M9**2)**(gamma_c/(gamma_c - 1))
        FF_m0 = alpha/(1 + alpha)*a0*(V19_a0 - M0 + T19_T0/V19_a0*(1 - 1/P19_P0)/gamma_c)
        FC_m0 = 1/(1 + alpha)*a0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t*T9_T0/(R_c*V9_a0)*(1 - 1/P9_P0)/gamma_c)
        F_m0 = FF_m0  + FC_m0
        S = f/((1 + alpha)*F_m0)
        N_NR_fan = (self.T0*tau_r/(T0_R*tau_r_R)*(pi_f**((gamma_c - 1)/gamma_c) - 1)/(pi_f_R**((gamma_c - 1)/gamma_c) - 1))**(1/2)
        N_NR_H = (self.T0*tau_r*tau_cL/(T0_R*tau_r_R*tau_cL_R)*(pi_cH**((gamma_c - 1)/gamma_c) - 1)/(pi_cH_R**((gamma_c - 1)/gamma_c) - 1))**(1/2)
        eta_T = a0**2*((1 + f)*V9_a0**2 + alpha*(V19_a0**2)- (1 + alpha)*M0**2)/(2*f*hpr*1000)
        eta_P = 2*V0*(1 + alpha)*F_m0/(a0**2*((1 + f)*V9_a0**2 + alpha*V19_a0**2 - (1 + alpha)*M0**2))
        eta_Total = eta_P*eta_T
        F = F_m0 * m0
        FC = S*F
        AF = 1/f
        mC = m0*1/(1 + alpha)
        mF = m0*alpha/(1 + alpha)
        tau_b = Tt9_T0/(tau_r*tau_d*tau_cH*tau_cL*tau_tH*tau_tL*tau_n)

        output = {
            'F_m0': [F_m0],
            'm0_dot': [m0],
            'f': [f],
            'S': [S],
            'eta_T': [eta_T],
            'eta_P': [eta_P],
            'eta_Total': [eta_Total],
            'alpha': [alpha],
            'pi_f': [pi_f],
            'pi_cH': [pi_cH],
            'pi_tL': [pi_tL],
            'tau_f': [tau_f],
            'tau_cH': [tau_cH],
            'tau_tL': [tau_tL],
            'M9': [M9],
            'M19': [M19],
            'N_fan': [N_NR_fan],
            'N_hp_spool': [N_NR_H],
            'm0_dot': [m0],
            'F': [F],
            'AF': [AF],
            'FC': [FC]
        }

        return output,self.T0,tau_cH_R,tau_cL_R,tau_r,pi_r,pi_d,tau_lambda,tau_tL,tau_f,tau_cL,pi_tL,pi_cL,tau_cH,pi_cH,pi_f,Pt19_P0,Pt19_P19,Pt9_P0,Pt9_P9,tau_f,tau_tL_R,tau_f_R,tau_cL_R,pi_tL_R,T9_T0,T19_T0,P19_P0,P9_P0,T9_Tt9,tau_b


#------------------------- RAMJET -------------------------------------------------------
    def ideal_ramjet(self, M0, gamma, cp, hpr, Tt4, A0 = 1):
        """
        Description: This method calculates the on design parameters of an ramjet turbojet engine.

        Arguments:
            M0: Mach number                             [  -  ]
            gamma: Ratio of specific heats              [  -  ]
            cp: Specific heat at constant pressure      [kJ/kgK]
            hpr: Low heating value of fuel              [kJ/kg]
            Tt4: Total temperature leaving the burner   [  K  ]

        Returns: A dictionary containing the list of calculated outputs.
            F_m0: Specific Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
        """

        output = {
            'F_m0': [],
        #    'F': [],
        #    'm0_dot': [],
            'f': [],
            'S': [],
        #    'FC': [],
            'Ar_Comb': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            #'FR': []
        }

        R = (gamma - 1)/gamma*cp*1000 # como foi multiplicado por 1000, agora está em J/(kg.K)

        a0 = (gamma*R*self.T0)**(1/2) #m/s
        V0 = M0*a0
        
        m0_dot = A0*self.rho0*V0
        
        tau_r = 1 + ((gamma - 1)/2)*(M0**2)

        tau_lambda = Tt4/self.T0
        V9_a0 = M0 * ((tau_lambda/tau_r)**0.5)

        F_m0 = a0 * (V9_a0 - M0)
        f = (cp * self.T0)/hpr * (tau_lambda - tau_r)
        S = f/F_m0
        
        F = F_m0*m0_dot
        
        FC = F/S
        AF = 1/f

        eta_T = 1 - 1/(tau_r)
        eta_P = 2/((tau_lambda/tau_r)**0.5 + 1)
        eta_Total = eta_P*eta_T

        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output

    def real_ramjet(self, M0, hpr, Tt4, A0, pi_b, pi_dmax, pi_n, P0_P9=1.0, gamma_c=1.4, gamma_t=1.4, cpc=1.004, cpt=1.004, eta_b=1.0):
        """
        Description: This method calculates the on design parameters of an ramjet turbojet engine.

        Arguments:
            M0: Mach number                             [  -  ]
            gamma: Ratio of specific heats              [  -  ]
            cp: Specific heat at constant pressure      [kJ/kgK]
            hpr: Low heating value of fuel              [kJ/kg]
            Tt4: Total temperature leaving the burner   [  K  ]

        Returns: A dictionary containing the list of calculated outputs.
            F_m0: Specific Thrust
            dot_m0: Air mass flow
            F: Thrust
            f: Fuel Air ratio
            S: Specific fuel consumption
            eta_T: Thermal efficiency
            eta_P: Propulsive efficiency
            eta_Total: Total efficiency
        """

        output = {
            'F_m0': [],
            'm0_dot':[],
            'F':[],
            'f': [],
            'S': [],
            'FC': [],
            'AF': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            #'FR': []
        }
        
        # Comentar sobre cpc 
        R_c = (gamma_c - 1)/gamma_c*cpc*1000 # como foi multiplicado por 1000, agora está em J/(kg.K)
        R_t = (gamma_t - 1)/gamma_t*cpt*1000

        a0 = (gamma_c*R_c*self.T0)**(1/2) #m/s
        V0 = a0*M0
        
        m0_dot = A0*self.rho0*V0
        
        tau_r = 1 + ((gamma_c - 1)/2)*(M0**2)
        pi_r  = tau_r**(gamma_c/(gamma_c-1))
        
        if M0 <= 1 or eta_b == 1:
            eta_r = 1
        else:
            eta_r = (1 - 0.075*(M0-1)**1.35)
            
        pi_d = eta_r*pi_dmax
        tau_d = pi_d**((gamma_c-1)/gamma_c)
        
        tau_lambda = cpt*Tt4/(self.T0*cpc)
        
        tau_n = 1
        
        tau_b = Tt4/(self.T0*tau_d*tau_r)
        # pi_b  = tau_b**(gamma_c/(gamma_c-1))
        
        Pt9_P9 = P0_P9*pi_r*pi_d*pi_b*pi_n
        P9 = self.P0/P0_P9
        Pt9 = Pt9_P9*P9
        
        M9 = (2/(gamma_t-1)*((Pt9/P9)**((gamma_t-1)/gamma_t)-1))**(1/2)
        #print(f"Mach 9 on design = {M9}")
        Tt9 = self.T0*tau_r*tau_d*tau_b*tau_n
        
        T9 = Tt9/(Pt9_P9**((gamma_t-1)/gamma_t))
        
        V9 = a0*M9*(gamma_t*R_t*T9/(gamma_c*R_c*self.T0))**(1/2)
        a9 = a0*(gamma_t*R_t*T9/(gamma_c*R_c*self.T0))**(1/2)
        
        f = (tau_lambda - tau_r*tau_d)/(eta_b*hpr/(cpc*self.T0) - tau_lambda + tau_r*tau_d)
        F_m0 = a0*((1+f)*V9/a0 - M0 + (1+f)*R_t*T9/self.T0*(1-P0_P9)/(R_c*V9/a0*gamma_c))
        F = F_m0*m0_dot
        S = f/F_m0
        
        F = F_m0*m0_dot
        
        FC = F*S
        
        AF = 1/f

        eta_T = (a0**2)*((1+f)*((V9/a0)**2) - (M0**2) )/(2*f*hpr*1000)
        eta_P = 2*V0*F_m0/( (a0**2)*((1+f)* ((V9/a0)**2) -M0**2)  )
        eta_Total = eta_P*eta_T

        # pi_n = (Pt9/self.P0)/(pi_r*pi_d*pi_b)

        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output,tau_lambda,tau_r,pi_r,tau_b,pi_b,pi_n,Pt9_P9,T9/Tt9,T9/self.T0,pi_d,tau_d

    def offdesign_ramjet(self,
        M0,
        Tt4,
        P0_P9,

        # Constantes
        gamma_c,
        cp_c,
        gamma_t,
        cp_t,
        hpr,
        pi_d_max,
        pi_b,
        pi_n,
        eta_b,

        # Condições de referência
        M0_R,
        T0_R,
        P0_R,
        tau_r_R,
        pi_r_R,
        Tt4_R,
        pi_d_R,
        Pt9_P9_R,

        #  Inputs extras do SA6 Gainful
        m0_R # kg/s (?)
        ):

        output = {
            'F_m0': [],
            'm0_dot':[],
            'F':[],
            'f': [],
            'S': [],
            'FC': [],
            'AF': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
        }

        T0 = self.T0
        P0 = self.P0

        Tt2_R = T0_R*tau_r_R


        #  Equations
        R_c = (gamma_c - 1)/gamma_c*cp_c*1000 # J/(kg.K)
        R_t = (gamma_t - 1)/gamma_t*cp_t*1000 # J/(kg.K)
        a0 = (gamma_c*R_c*T0)**(1/2) # m/s
        V0 = a0*M0

        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35

        pi_d = pi_d_max*eta_r
        tau_d = pi_d**((gamma_c-1)/gamma_c)
        
        Tt2 = T0*tau_r
        
        # Ramjet simplifications
        tau_c   = 1
        pi_c    = 1
        pi_c_R  = 1
        
        pi_t    = 1
        
        tau_n = 1
        
        tau_lambda = cp_t*Tt4/(cp_c*T0)
        f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*T0) - tau_lambda) # kgFuel/kgAir
        m0_dot = m0_R*P0*pi_r*pi_d*pi_c/(P0_R*pi_r_R*pi_d_R*pi_c_R)*(Tt4_R/Tt4)**(1/2) # kg/s

        Pt9_P9 = P0_P9*pi_r*pi_d*pi_c*pi_b*pi_t*pi_n
        M9 = (2/(gamma_t - 1)*(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
        #print(f"Mach 9 off design = {M9}")
        T9_T0 = Tt4/T0/(Pt9_P9)**((gamma_t - 1)/gamma_t)
        
        V9_a0 = M9*(gamma_t*R_t/(gamma_c*R_c)*T9_T0)**(1/2)
        F_m0 = a0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t*T9_T0/(R_c*V9_a0)*(1 - P0_P9)/gamma_c) # N/(kg/s)
        F = F_m0*m0_dot # N
        S = f/F_m0 # (kgFuel/s)/N
        eta_T = a0**2*((1 + f)*V9_a0**2 - M0**2)/(2*f*hpr*1000)
        eta_P = 2*V0*F_m0/(a0**2*((1 + f)*V9_a0**2 - M0**2))
        eta_Total = eta_P*eta_T
        N_NR = (T0*tau_r/(T0_R*tau_r_R)*(pi_c**((gamma_c - 1)/gamma_c) - 1)/(pi_c_R**((gamma_c - 1)/gamma_c) - 1))**(1/2)
        A9_A9R = (Pt9_P9/Pt9_P9_R)**((gamma_t + 1)/(2*gamma_t))*((Pt9_P9_R**((gamma_t - 1)/gamma_t) - 1)/(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
        mc2_mc2_R = pi_c/pi_c_R*((Tt4_R/Tt2_R)/(Tt4/Tt2))**(1/2) # vazão mássica corrigida no compressor

        #  Outputs extras
        tau_b = Tt4/(self.T0*tau_d*tau_r)
        Tt9 = self.T0*tau_r*tau_d*tau_b*tau_n
        V9 = V9_a0*a0 # m/s
        AF = 1/f  # kgAir/kgFuel
        Pt4 = P0*pi_r*pi_d*pi_c*pi_b # Pa
        Pt9 = P0*pi_r*pi_d*pi_c*pi_b*pi_t # Pa
        T9 = T0*T9_T0 # K
        FC = F/S

        output['F_m0'].append(F_m0)
        output['m0_dot'].append(m0_dot)
        output['F'].append(F)
        output['f'].append(f)
        output['S'].append(S)
        output['FC'].append(FC)
        output['AF'].append(AF)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        
        return output,tau_lambda,tau_r,pi_r,tau_b,pi_b,pi_n,Pt9_P9,T9/Tt9,T9/self.T0,pi_d,tau_d



#-------------------------------------------- TURBOPROP --------------------------------------------------
    def ideal_turboprop(self, M0, gamma, cp, hpr, Tt4, pi_c, tau_t, eta_prop):

        output = {
        'pi_c': [],
        'F_m0': [],
        'f': [],
        'S': [],
        'eta_T': [],
        'eta_P': [],
        'eta_Total': [],
        'C_c': [],
        'C_prop': [],
        'C_tot': [] #C_Total -> C_tot
        }

        R = (gamma - 1)/gamma*cp*1000
        a0 = (gamma*R*self.T0)**(1/2)
        V0 = a0*M0 #m/s
        
        tau_r = 1 + (gamma - 1)/2*M0**2
        tau_lambda = Tt4/self.T0
        tau_c = pi_c**((gamma - 1)/(gamma))
        
        f = cp*self.T0*(tau_lambda - tau_r*tau_c)/hpr
        
        tau_tH = 1 - tau_r/tau_lambda*(tau_c - 1)
        tau_tL = tau_t/tau_tH
        
        pi_r = tau_r**(gamma/(gamma - 1))
        pi_tH = tau_tH**(gamma/(gamma - 1))

        V9_a0 = (2/(gamma - 1)*(tau_lambda*tau_t - tau_lambda/(tau_r*tau_c)))**0.5
        T9_T0 = tau_lambda/(tau_r*tau_c)
        M9 = (2/(gamma-1)*(tau_r*tau_c*tau_tH*tau_tL - 1))**0.5
        
        C_c = (gamma - 1)*M0*(V9_a0 - M0)
        C_prop = eta_prop*tau_lambda*tau_tH*(1 - tau_tL)
        C_tot = C_prop + C_c
        
        F_m0 = C_tot*cp*self.T0/(M0*a0)
        
        S = f/F_m0
        S_P = f/(C_tot*cp*self.T0)
        
        eta_T = 1 - 1/(tau_r*tau_c)
        eta_Total = C_tot/(tau_lambda - tau_r*tau_c)
        eta_P = eta_Total/eta_T
        
        pi_d = 1 #
        tau_d = 1 #
        pi_b = 1 #
        tau_b = Tt4/(self.T0*tau_d*tau_r*tau_c) #
        pi_tL = tau_tL**(gamma/((gamma-1))) #
        pi_n = 1 #
        tau_n = 1 #
        P0_P9 = 1 #
        Pt9_P0 = pi_r*pi_d*pi_c*pi_b*pi_tH*pi_tL*pi_n #
        Pt9_P9 = Pt9_P0  #

        Tt9_T0 = tau_lambda*tau_tH*tau_tL #
        T9_Tt9 = T9_T0/Tt9_T0 #
        AF = 1/f
        
        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        output['C_c'].append(C_c)
        output['C_prop'].append(C_prop)
        output['C_tot'].append(C_tot)

        return output,tau_lambda,pi_r,tau_r,pi_d,tau_d,pi_c,tau_c,pi_b,tau_b,pi_tH,tau_tH,pi_tL,tau_tL,pi_n,tau_n,P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
              #output,tau_lambda,pi_r,tau_r,pi_d,tau_d,pi_c,tau_c,pi_b,tau_b,pi_tH,tau_tH,pi_tL,tau_tL,pi_n,tau_n,P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
    def real_turboprop(self,
        M0,
        Tt4,
        #P0_P9, #Comentado por Gabriel

        # Constantes
        gamma_c,
        cp_c,
        gamma_t,
        cp_t,
        hpr,
        pi_d_max,
        pi_b,
        pi_n,
        pi_c,
        e_c,
        e_tH,
        e_tL,
        #tau_tH, Comentado por Gabriel
        tau_t,
        eta_b,
        eta_mL,
        eta_mH,
        eta_g,
        eta_prop,
        #m0_dot, #Para calcular m0_dot. Caso queira inserir diretamente m0_dot "a gente" muda depois # Comentado podr Gabriel

        ):
        output = {
        'pi_c': [],
        'F_m0': [],
        'f': [],
        'S': [],
        'eta_T': [],
        'eta_P': [],
        'eta_Total': [],
        'C_c': [],
        'C_prop': [],
        'C_tot': [], #C_Total -> C_tot
        'W_m0': [],
        'S_P': [],
        'm0_dot': [] #Adicionado por Gabriel
        }
        
        R_c = 1000*(gamma_c - 1)/gamma_c*cp_c
        R_t = 1000*(gamma_t - 1)/gamma_t*cp_t
        a0 = (gamma_c*R_c*self.T0)**(1/2)
        V0 = a0*M0
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))
        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1-0.0075*(M0-1)**1.35
        
        pi_d = pi_d_max*eta_r
        tau_d = pi_d**((gamma_c-1)/gamma_c) #adicionado Gabriel
        tau_n = 1 #adicionado Gabriel
        tau_lambda = cp_t*Tt4/(cp_c*self.T0)
        tau_c = pi_c**((gamma_c - 1)/(gamma_c*e_c))
        tau_b = Tt4/(self.T0*tau_d*tau_r*tau_c) #adicionado Gabriel
        eta_c = (pi_c**((gamma_c - 1)/gamma_c) - 1)/(tau_c - 1)
        
        f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*self.T0) - tau_lambda)
        
        tau_tH = 1 - tau_r*(tau_c - 1)/(eta_mH*(1 + f)*tau_lambda)
        pi_tH = tau_tH**(gamma_t/((gamma_t - 1)*e_tH))
        eta_tH = (1 - tau_tH)/(1 - tau_tH**(1/e_tH))
        
        tau_tL = tau_t/tau_tH
        
        pi_tL = tau_tL**(gamma_t/((gamma_t-1)*e_tL))
        eta_tL = (1-tau_tL)/(1-tau_tL**(1/e_tL))
        
        Pt9_P0 = pi_r*pi_d*pi_c*pi_b*pi_tH*pi_tL*pi_n
        
        if Pt9_P0 > ((gamma_t+1)/2)**(gamma_t/(gamma_t-1)):
            M9 = 1
            Pt9_P9 = ((gamma_t+1)/2)**(gamma_t/(gamma_t-1))
            P0_P9 = Pt9_P9/Pt9_P0
        else:
            M9 = (2/(gamma_t-1)*(Pt9_P0**((gamma_t-1)/gamma_t)-1))**0.5
            Pt9_P9 = Pt9_P0
            P0_P9 = 1
            
        V9_a0 = (2*tau_lambda*tau_tH*tau_tL/(gamma_c - 1)*(1 - (Pt9_P9)**(-1*(gamma_t - 1)/gamma_t)))**0.5
        Tt9_T0 = Tt4/self.T0*tau_tH*tau_tL
        T9_T0 = Tt9_T0/(Pt9_P9**((gamma_t-1)/gamma_t))
        T9_Tt9 = T9_T0/Tt9_T0 #adicionado Gabriel
        
        C_prop = eta_prop*eta_g*eta_mL*(1 + f)*tau_lambda*tau_tH*(1 - tau_tL)
        C_c = (gamma_c - 1)*M0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t/R_c*T9_T0/V9_a0*(1 - P0_P9)/gamma_c)
        
        C_tot = C_prop + C_c
        
        F_m0 = C_tot*cp_c*1000*self.T0/V0 # multipliquei por 1000 aqui por causa do cp
        S = f/F_m0
        S_P = f/(C_tot*cp_c*1000*self.T0) # multipliquei por 1000 aqui por causa do cp

        W_m0 = C_tot*cp_c*self.T0

        eta_P = C_tot/(C_prop/eta_prop + ((gamma_c - 1)/2)*((1 + f)*V9_a0**2 - M0**2))
        eta_T = C_tot*cp_c*self.T0/(f*hpr)
        eta_Total = eta_P*eta_T
        AF = 1/f

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        output['C_c'].append(C_c)
        output['C_prop'].append(C_prop)
        output['C_tot'].append(C_tot)
        output['W_m0'].append(W_m0)
        output['S_P'].append(S_P)
        #output['m0_dot'].append(m0_dot) #Adicionado por Gabriel

        return output,tau_lambda,pi_r,tau_r,pi_d,tau_d,pi_c,tau_c,pi_b,tau_b,pi_tH,tau_tH,pi_tL,tau_tL,pi_n,tau_n,P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
    
    def offdesign_turboprop(self,
        M0,
        Tt4,
        #P0_P9,

        # Constantes
        gamma_c,
        cp_c,
        gamma_t,
        cp_t,
        hpr,
        pi_d_max,
        pi_b,
        pi_tH,
        pi_n,
        tau_tH,
        eta_c,
        eta_b,
        eta_tL,
        eta_mL,
        eta_g,
        eta_propmax,

        # Condições de referência
        M0_R,
        T0_R,
        P0_R,
        m0_dot_R,
        tau_r_R,
        pi_r_R,
        Tt4_R,
        pi_d_R,
        pi_c_R,
        tau_c_R,
        pi_tL_R,
        tau_tL_R,
        M9_R,
        Pt9_P9_R,
        ):

        output = {
        'pi_c': [],
        'F_m0': [],
        'f': [],
        'S': [],
        'eta_T': [],
        'eta_P': [],
        'eta_Total': [],
        'C_c': [],
        'C_prop': [],
        'C_tot': [], #C_Total -> C_tot
        'W_m0': [],
        'S_P': [],
        'F': [],
        'm0_dot': []
        }
        
        if M0 <= 0.1:
            eta_prop = 10*M0*eta_propmax
        elif M0 <= 0.7:
            eta_prop = eta_propmax
        else:
            eta_prop = (1-(M0-0.7)/3)*eta_propmax
        

        R_c = 1000*(gamma_c - 1)/gamma_c*cp_c
        R_t = 1000*(gamma_t - 1)/gamma_t*cp_t
        a0 = (gamma_c*R_c*self.T0)**(1/2)
        V0 = a0*M0
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))
        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35
        pi_d = pi_d_max*eta_r

        tau_c = 1 + (Tt4/self.T0)/(Tt4_R/T0_R)*(tau_r_R/tau_r)*(tau_c_R-1)
        pi_c = (1+eta_c*(tau_c-1))**(gamma_c/(gamma_c-1))
        tau_lambda = cp_t*Tt4/(cp_c*self.T0)
        
        f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*self.T0) - tau_lambda)
        m0_dot = m0_dot_R*(self.P0*pi_r*pi_d*pi_c)/(P0_R*pi_r_R*pi_d_R*pi_c_R)*(Tt4_R/Tt4)**(0.5)

        pi_tL = pi_tL_R
        pi_tL_prev = 0
        

        while abs(pi_tL - pi_tL_prev) > 0.0001:
            tau_tL = 1 - eta_tL*(1-pi_tL**((gamma_t-1)/gamma_t))
            Pt9_P0 = pi_r*pi_d*pi_c*pi_b*pi_tH*pi_tL*pi_n
            if Pt9_P0 >= ((gamma_t+1)/2)**(gamma_t/(gamma_t-1)):
                M9 = float(1)
                Pt9_P9 = ((gamma_t+1)/2)**(gamma_t/(gamma_t-1))
                P0_P9 = Pt9_P9/Pt9_P0
            else:
                P0_P9 = 1
                Pt9_P9 = Pt9_P0
                M9 = (2/(gamma_t-1)*(Pt9_P0**((gamma_t-1)/gamma_t)-1) )**0.5

            MFP = M9*((gamma_t/R_t)**0.5)/((1+(M9**2)*((gamma_t-1)/2))**( (gamma_t+1)/(2*(gamma_t-1)) ))
            MFP_R = M9_R*((gamma_t/R_t)**0.5)/((1+(M9_R**2)*((gamma_t-1)/2))**( (gamma_t+1)/(2*(gamma_t-1)) ))
            pi_tL_prev = pi_tL
            pi_tL = pi_tL_R*((tau_tL/tau_tL_R)**0.5)*MFP_R/MFP

        

        T9 = Tt4*tau_tH*tau_tL/( Pt9_P9**((gamma_t-1)/gamma_t) )  
        T9_T0 = T9/self.T0


        V9_a0 = M9*(gamma_t*R_t*T9/(gamma_c*R_c*self.T0))**0.5

        
        C_c = (gamma_c - 1)*M0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t/R_c*T9_T0/V9_a0*(1 - P0_P9)/gamma_c)

        C_prop = eta_prop*eta_g*eta_mL*(1 + f)*tau_lambda*tau_tH*(1 - tau_tL)
        C_tot = C_c + C_prop
        
        F_m0 = C_tot*cp_c*1000*self.T0/V0 #multipliquei por 1000 aqui por causa do cp
        S = f/F_m0
        S_P = f/(C_tot*cp_c*1000*self.T0) #multipliquei por 1000 aqui por causa do cp
        
        F = F_m0*m0_dot

        W_m0 = C_tot*cp_c*self.T0

        tau_d = pi_d**((gamma_c-1)/gamma_c) #adicionado Gabriel
        tau_b = Tt4/(self.T0*tau_d*tau_r*tau_c) #adicionado Gabriel
        tau_n = 1 #adicionado Gabriel
        Tt9_T0 = Tt4/self.T0*tau_tH*tau_tL  #adicionado Gabriel
        T9_Tt9 = T9_T0/Tt9_T0 #adicionado Gabriel

        eta_P = C_tot/(C_prop/eta_prop + ((gamma_c - 1)/2)*((1 + f)*V9_a0**2 - M0**2))
        eta_T = C_tot*cp_c*self.T0/(f*hpr)
        eta_Total = eta_P*eta_T
        AF = 1/f

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['F'].append(F)
        output['m0_dot'].append(m0_dot)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        output['C_c'].append(C_c)
        output['C_prop'].append(C_prop)
        output['C_tot'].append(C_tot)
        output['W_m0'].append(W_m0)
        output['S_P'].append(S_P)
        


        return output,tau_lambda,pi_r,tau_r,pi_d,tau_d,pi_c,tau_c,pi_b,tau_b,pi_tH,tau_tH,pi_tL,tau_tL,pi_n,tau_n,P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
