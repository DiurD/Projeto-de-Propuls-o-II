from ambiance import Atmosphere
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

class AircraftEngines:

    def __init__(self, height):
        self.atm = Atmosphere(height)
        self.T0 = self.atm.temperature[0]
        self.P0 = self.atm.pressure[0]
        self.a0 = self.atm.speed_of_sound[0]

    def __str__(self):
        return f"\nDados atmosféricos:\nT0 = {self.T0} K \nP0 = {self.P0} Pa\na0 = {self.a0} m/s\n"

    def set_param(self,new_T0,new_P0,new_a0):
        self.T0 = new_T0
        self.P0 = new_P0
        self.a0 = new_a0
        





#--------------------------- TURBOJET --------------------------------------------------


    def ideal_turbojet(self, M0, gamma, cp, hpr, Tt4, pi_c, batch_size=1, min_pi_c=0.001, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an ideal turbojet engine.

        Arguments:
            M0: Mach number                                     [  -  ]
            gamma: Ratio of specific heats                      [kJ/kgK]
            cp: Specific heat at constant pressure              [ J/K ]
            hpr: Low heating value of fuel                      [kJ/kg]
            Tt4: Total temperature leaving the burner           [  K  ]
            pi_c: Compressor total pressure ratio               [  -  ]
            batch_size: Number of points to iterate pi_c        [  -  ]
            min_pi_c: Min value for pi_c (only used in batch)   [  -  ]
            max_pi_c: Max value for pi_c (only used in batch)   [  -  ]

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
            'eta_Total': []
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

            R = (gamma - 1)/gamma * cp  # eq 5.18a
            V0 = self.a0 * M0

            tau_r = 1 + (gamma - 1)/2 * M0**2  # eq 5.18c

            tau_c = pi_c**((gamma - 1)/gamma) # assumption ideal cycle
            
            tau_lambda = Tt4/self.T0  # eq 5.18d
            f = cp * self.T0/hpr * (tau_lambda - tau_r * tau_c)  # eq 5.25

            tau_t = 1 - tau_r/tau_lambda * (tau_c - 1)  # eq 5.27
            V9_a0 = (2/(gamma - 1 )* tau_lambda/(tau_r * tau_c) * (tau_r * tau_c * tau_t - 1))**(1/2)  # eq 5.28

            F_m0 = self.a0 * (V9_a0 - M0)  # eq 5.29
            S = f/F_m0  # eq 5.8
            eta_T = 1 - 1/(tau_r * tau_c)  # eq 5.31a
            eta_P = 2 * M0/(V9_a0 + M0)  # eq 5.31b
            eta_Total = eta_P * eta_T # eq 5.31c

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            # output['pi_c'][0]
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)

            pi_c += pi_c_increase

        return output



    def ideal_turbojet_with_afterburner(self, M0, gamma, cp, hpr, Tt4, Tt7, pi_c, batch_size=1, min_pi_c=0.001, max_pi_c=40):

        """
              Description: This method implements afterburner on the ideal turbojet analysis

              Arguments:
                  M0: Mach number                                     [  -  ]
                  gamma: Ratio of specific heats                      [kJ/kgK]
                  cp: Specific heat at constant pressure              [ J/K ]
                  hpr: Low heating value of fuel                      [kJ/kg]
                  Tt4: Total temperature leaving the burner           [  K  ]
                  Tt7: Total temperature leaving the afterburner           [  K  ]
                  pi_c: Compressor total pressure ratio               [  -  ]
                  batch_size: Number of points to iterate pi_c        [  -  ]
                  min_pi_c: Min value for pi_c (only used in batch)   [  -  ]
                  max_pi_c: Max value for pi_c (only used in batch)   [  -  ]

                  Novos:



              Returns: A dictionary containing the list of calculated outputs for each batch.
                  pi_c: Compressor total pressure ratio
                  F_m0: Specific Thrust
                  f_tot: Fuel Air ratio including the afterburner
                  S: Specific fuel consumption
                  eta_T: Thermal efficiency
                  eta_P: Propulsive efficiency
                  eta_Total: Total efficiency
              """

        output = {
            'pi_c': [],
            'F_m0': [],
            'f_tot': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': []
        }

        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:

            R = (gamma - 1) / gamma * cp  # eq 5.18a
            V0 = self.a0 * M0

            tau_r = 1 + (gamma - 1) / 2 * M0 ** 2  # eq 5.18c

            tau_c = pi_c ** ((gamma - 1) / gamma)  # assumption ideal cycle

            tau_lambda = Tt4 / self.T0  # eq 5.18d
            f = cp * self.T0 / hpr * (tau_lambda - tau_r * tau_c)  # eq 5.25

            tau_t = 1 - tau_r / tau_lambda * (tau_c - 1)  # eq 5.27


            V9_a0_dry = (2 / (gamma - 1) * tau_lambda / (tau_r * tau_c) * (tau_r * tau_c * tau_t - 1)) ** (1 / 2)  # eq 5.28


            #A partir daqui começa a modifição para incluir o afterburner:

            tau_lambda_AB = Tt7 / self.T0  # eq 5.38

            Tt9_Tt5 = tau_lambda_AB / (tau_lambda * tau_t) # eq 5.39

            V9_a0_AB =  ( Tt9_Tt5 * V9_a0_dry**2 ) ** (1/2) #eq  5.37

            V9_a0_AB = ( (2 / (gamma - 1)) * tau_lambda_AB * ( 1 - (tau_lambda / (tau_r*tau_c) )/ ( tau_lambda - tau_r*(tau_c -1)))  )**(1/2)# eq. 5.40

            f_tot = (cp* self.T0 / hpr)*(tau_lambda_AB - tau_r) # eq. 5.41
            eta_T =  (((gamma - 1) * cp * self.T0) * (V9_a0_AB**2 - M0**2)) / (2*f_tot*hpr)
            F_m0 = self.a0 * (V9_a0_AB - M0)
            S = f_tot / F_m0
            eta_P = 2 * M0 / (V9_a0_AB + M0)
            eta_Total = eta_P * eta_T

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f_tot) or math.isnan(eta_P) or math.isnan(
                    eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f_tot'].append(f_tot)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)

            pi_c += pi_c_increase

        return output
    
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



    def real_turbojet(self, M0, gamma_c, gamma_t, cp_c, cp_t, hpr, Tt4 , pi_c, pi_d_max, pi_b, pi_n, e_c, e_t, eta_b, eta_m, P0_P9, batch_size=1, min_pi_c=0.001, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an non ideal turbojet engine.

        Arguments:
            M0: Mach number
            gamma_c: Ratio of specific heats in the compressor          [kJ/kgK]
            gamma_t: Ratio of specific heats in the turbine             [kJ/kgK]
            cp_c: Specific heat at constant pressure in the compressor  [ J/K ]
            cp_t: Specific heat at constant pressure in the turbine     [ J/K ]
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
        """

        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': []
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

            # Gas constants
            R_c    = ((gamma_c - 1)/gamma_c ) * (cp_c)
            R_t    = ((gamma_t - 1)/gamma_t ) * (cp_t)

            # Free stream
            a0    = math.sqrt(gamma_c*R_c*self.T0)
            V0    = a0 * M0

            # Free flow parameters
            tal_r    = 1 + ((gamma_c - 1)/2 ) * (M0**2)
            pi_r     = tal_r**(gamma_c/(gamma_c - 1))

            if (M0 <= 1):
                eta_r  = 1
            elif (M0 > 1 and M0 <= 5):
                eta_r  = 1 - 0.075*((M0 - 1)**(1.35))
            elif (M0 > 5):
                eta_r  = 800/(M0**4 + 935)

            # Diffuser
            pi_d   = pi_d_max*eta_r

            # Compressor
            tal_c    = (pi_c)**((gamma_c - 1)/(gamma_c*e_c))
            eta_c    = (pi_c**((gamma_c - 1)/gamma_c) - 1)/(tal_c - 1)

            # Burner
            tal_lambda    = cp_t*Tt4/(cp_c*self.T0)
            f             = (tal_lambda-tal_r*tal_c)/( (hpr*eta_b/(cp_c*self.T0)) - tal_lambda)

            # Turbine
            tal_t  = 1 - (1/(eta_m*(1+f)))*(tal_r/tal_lambda)*(tal_c-1)
            pi_t   = tal_t**(gamma_t/((gamma_t-1)*e_t))
            eta_t  = (1 - tal_t)/(1 - tal_t**(1/e_t))

            # Auxiliar
            Pt9_P9 = (P0_P9)*pi_r*pi_d*pi_c*pi_b*pi_t*pi_n
            M9     = (2/(gamma_t - 1)*(Pt9_P9**((gamma_t - 1)/gamma_t) - 1))**(1/2)
            T9_T0  = (tal_lambda*tal_t)/( ((Pt9_P9)**((gamma_t-1)/gamma_t)))*(cp_c/cp_t)
            V9_a0  = M9*( math.sqrt( gamma_t*R_t*(T9_T0)/(gamma_c*R_c) ) )

            # Results
            F_m0      = a0*((1+f)*V9_a0 - M0 + (1+f)*R_t*T9_T0/(R_c*V9_a0)*(1-P0_P9)/gamma_c)
            S         = f/F_m0
            eta_T     = ((a0**2)*( (1+f)*V9_a0**2 - M0**2 )/(2*f*(hpr)))
            eta_P     = ( 2*V0*F_m0/( (a0**2)*( (1+f)*V9_a0**2 - M0**2 ) ) )
            eta_Total = eta_T*eta_P

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

            pi_c += pi_c_increase

        return output


    def real_turbojet_with_afterburner(self, M0, gamma_c, gamma_t, gamma_AB, cp_c, cp_t, cp_AB, hpr, Tt4, Tt7,pi_c, pi_d_max, pi_b, pi_n, pi_AB, e_c, e_t, eta_b, eta_AB, eta_m, P0_P9, AB, batch_size=10, min_pi_c=1.1, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an non ideal turbojet engine.

        Arguments:
            M0: Mach number
            gamma_c: Ratio of specific heats in the compressor          [kJ/kgK]
            gamma_t: Ratio of specific heats in the turbine             [kJ/kgK]
            cp_c: Specific heat at constant pressure in the compressor  [ J/K ]
            cp_t: Specific heat at constant pressure in the turbine     [ J/K ]
            hpr: Low heating value of fuel                              [kJ/kg]
            Tt4: Total temperature leaving the burner                   [  K  ]
            pi_c: Compressor total pressure ratio                       [  -  ]
            pi_d_max: Diffuser maximum total pressure ratio              [  -  ]
            pi_b: Burner total pressure ratio                           [  -  ]
            pi_n: Nozzle total pressure ratio                           [  -  ]
            e_t: Polytropic compressor efficiency                       [  -  ]
            e_t: Polytropic turbine efficiency                          [  -  ]
            eta_b: Combustor efficiency                                 [  -  ]
            eta_m: Mechanical efficiency                                [  -  ]
            P0_P9: Ratio between Po/P9                                  [  -  ]
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
        """

        output = {
            'pi_c': [],
            'F_m0': [],
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': []
        }

        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
           max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:
            # Gas constants
            R_c = ((gamma_c - 1) / gamma_c) * cp_c
            R_t = ((gamma_t - 1) / gamma_t) * cp_t

            # Free stream
            a0 = math.sqrt(gamma_c * R_c * self.T0)
            V0 = a0 * M0

            # Free flow parameters
            tal_r = 1 + ((gamma_c - 1) / 2) * (M0 ** 2)
            pi_r = tal_r ** (gamma_c / (gamma_c - 1))

            if M0 <= 1:
                eta_r = 1
            elif M0 > 1 and M0 <= 5:
                eta_r = 1 - 0.075 * ((M0 - 1) ** (1.35))
            elif M0 > 5:
                eta_r = 800 / (M0 ** 4 + 935)

            # Diffuser
            pi_d = pi_d_max * eta_r

            # Compressor
            tal_c = (pi_c) ** ((gamma_c - 1) / (gamma_c * e_c))
            eta_c = (pi_c ** ((gamma_c - 1) / gamma_c) - 1) / (tal_c - 1)

            # Burner
            tal_lambda = cp_t * Tt4 / (cp_c * self.T0)
            f = (tal_lambda - tal_r * tal_c) / ((hpr * eta_b / (cp_c * self.T0)) - tal_lambda)

            # Turbine
            tal_t = 1 - (1 / (eta_m * (1 + f))) * (tal_r / tal_lambda) * (tal_c - 1)
            pi_t = tal_t ** (gamma_t / ((gamma_t - 1) * e_t))
            eta_t = (1 - tal_t) / (1 - tal_t ** (1 / e_t))

            # if 'AB' = 0, afterburner is off
            if AB == 0:
                # Auxiliar
                Pt9_P9 = (P0_P9) * pi_r * pi_d * pi_c * pi_b * pi_t * pi_n
                M9 = (2 / (gamma_t - 1) * (Pt9_P9 ** ((gamma_t - 1) / gamma_t) - 1)) ** (1 / 2)
                T9_T0 = (tal_lambda * tal_t) / (((Pt9_P9) ** ((gamma_t - 1) / gamma_t))) * (cp_c / cp_t)
                V9_a0 = M9 * (math.sqrt(gamma_t * R_t * (T9_T0) / (gamma_c * R_c)))

                # Results
                F_m0 = a0 * ((1 + f) * V9_a0 - M0 + (1 + f) * R_t * T9_T0 / (R_c * V9_a0) * (1 - P0_P9) / gamma_c)
                S = f / F_m0
                eta_T = ((a0 ** 2) * ((1 + f) * V9_a0 ** 2 - M0 ** 2) / (2 * f * (hpr)))
                eta_P = (2 * V0 * F_m0 / ((a0 ** 2) * ((1 + f) * V9_a0 ** 2 - M0 ** 2)))
                eta_Total = eta_T * eta_P

                if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                        eta_T) or math.isnan(eta_Total):
                    pi_c += pi_c_increase
                    continue

                output['pi_c'].append(pi_c)
                output['F_m0'].append(F_m0)
                output['f'].append(f)
                output['S'].append(S)
                output['eta_T'].append(eta_T)
                output['eta_P'].append(eta_P)
                output['eta_Total'].append(eta_Total)

                pi_c += pi_c_increase

            else:
                # Gas constants
                R_AB = ((gamma_AB - 1) / gamma_AB) * cp_AB

                # Afterburner
                tal_lambda_AB = cp_AB * Tt7 / (cp_c * self.T0)
                f_AB = (1 + f) * (tal_lambda_AB - tal_lambda * tal_t) / (
                        (hpr * eta_AB / (cp_c * self.T0)) - tal_lambda_AB)

                # Auxiliar
                Pt9_P9 = (P0_P9) * pi_r * pi_d * pi_c * pi_b * pi_t * pi_n * pi_AB
                T9_T0 = (Tt7 / self.T0) / (((Pt9_P9) ** ((gamma_AB - 1) / gamma_AB)))
                M9 = (2 / (gamma_AB - 1) * (Pt9_P9 ** ((gamma_AB - 1) / gamma_AB) - 1)) ** (1 / 2)
                V9_a0 = M9 * (math.sqrt(gamma_AB * R_AB * (T9_T0) / (gamma_c * R_c)))

                # Results
                F_m0 = a0 * ((1 + f + f_AB) * V9_a0 - M0 + (1 + f + f_AB) * R_AB * T9_T0 / (R_c * V9_a0) * (
                        1 - P0_P9) / gamma_c)
                S = (f + f_AB) / F_m0
                eta_T = ((a0 ** 2) * ((1 + f + f_AB) * V9_a0 ** 2 - M0 ** 2) / (2 * (f_AB + f) * (hpr)))
                eta_P = (2 * V0 * F_m0 / ((a0 ** 2) * ((1 + f + f_AB) * V9_a0 ** 2 - M0 ** 2)))
                eta_Total = eta_T * eta_P

                if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                        eta_T) or math.isnan(eta_Total):
                    pi_c += pi_c_increase
                    continue

                output['pi_c'].append(pi_c)
                output['F_m0'].append(F_m0)
                output['f'].append(f)
                output['S'].append(S)
                output['eta_T'].append(eta_T)
                output['eta_P'].append(eta_P)
                output['eta_Total'].append(eta_Total)

                pi_c += pi_c_increase

        return output


    def real_turbojet_off_design(self,
        M0,
        Tt4,
        Tt7,
        P0_P9,
        AB,

        # Constantes
        gamma_c,
        cp_c,
        gamma_t,
        cp_t,
        gamma_AB,
        cp_AB,
        hpr,
        pi_d_max,
        pi_b,
        pi_t,
        pi_AB,
        pi_n,
        tau_t,
        eta_c,
        eta_b,
        eta_AB,
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
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': []
        }

        T0 = self.T0
        P0 = self.P0

        Tt2_R = T0_R*tau_r_R


        #  Equations
        R_c = (gamma_c - 1)/gamma_c*cp_c # J/(kg.K)
        R_t = (gamma_t - 1)/gamma_t*cp_t # J/(kg.K)
        a0 = (gamma_c*R_c*T0)**(1/2) # m/s
        V0 = a0*M0
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35

        pi_d = pi_d_max*eta_r
        Tt2 = T0*tau_r
        tau_c = 1 + (tau_c_R - 1)*Tt4/Tt2/(Tt4_R/Tt2_R)
        pi_c = (1 + eta_c*(tau_c - 1))**(gamma_c/(gamma_c - 1))
        tau_lambda = cp_t*Tt4/(cp_c*T0)
        f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*T0) - tau_lambda) # kgFuel/kgAir
        m0 = m0_R*P0*pi_r*pi_d*pi_c/(P0_R*pi_r_R*pi_d_R*pi_c_R)*(Tt4_R/Tt4)**(1/2) # kg/s

        if AB != 1:
            #  Without afterburner (dry)
            R_AB = R_t
            cp_AB = cp_t
            gamma_AB = gamma_t
            Tt7 = Tt4*tau_t
            pi_AB = 1
            f_AB = 0
        else:
            #  With afterburner (wet)
            R_AB = (gamma_AB - 1)/gamma_AB*cp_AB # J/(kg.K)
            tau_lambda_AB = cp_AB*Tt7/(cp_c*T0)
            f_AB = (tau_lambda_AB - tau_lambda*tau_t)/(hpr*eta_AB/(cp_c*T0) - tau_lambda_AB) # kgFuel/kgAir


        Pt9_P9 = P0_P9*pi_r*pi_d*pi_c*pi_b*pi_t*pi_AB*pi_n
        M9 = (2/(gamma_AB - 1)*(Pt9_P9**((gamma_AB - 1)/gamma_AB) - 1))**(1/2)
        T9_T0 = Tt7/T0/(Pt9_P9)**((gamma_AB - 1)/gamma_AB)
        V9_a0 = M9*(gamma_AB*R_AB/(gamma_c*R_c)*T9_T0)**(1/2)
        f_Total = f + f_AB
        F_m0 = a0*((1 + f_Total)*V9_a0 - M0 + (1 + f_Total)*R_AB*T9_T0/(R_c*V9_a0)*(1 - P0_P9)/gamma_c) # N/(kg/s)
        F = F_m0*m0 # N
        S = f_Total/F_m0 # (kgFuel/s)/N
        eta_T = a0**2*((1 + f_Total)*V9_a0**2 - M0**2)/(2*f_Total*hpr)
        eta_P = 2*V0*F_m0/(a0**2*((1 + f_Total)*V9_a0**2 - M0**2))
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

        output['pi_c'].append(pi_c)
        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output



#------------------------------- TURBOFAN ------------------------------------------------------------

    def ideal_turbofan(self, M0, gamma, cp, hpr, Tt4, pi_c, pi_f, alpha, batch_size=1, min_pi_c=0.001, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an ideal turbofan engine.

        Arguments:
            M0: Mach number                                             [  -  ]
            gamma: Ratio of specific heats                              [kJ/kgK]
            cp: Specific heat at constant pressure                      [ J/K ]
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
            tau_f = pi_f**((gamma - 1)/gamma) # eq 5.58f
            V19_a0 = (2/(gamma - 1) * (tau_r * tau_f - 1))**(1/2) # eq 5.58h
            tau_c = pi_c**((gamma - 1)/gamma)  # assumption ideal cycle # eq 5.58e
            tau_lambda = Tt4/self.T0 # eq 5.58d
            f = cp * self.T0/hpr * (tau_lambda - tau_r * tau_c) # eq 5.58j
            tau_t = 1 - tau_r/tau_lambda * (tau_c - 1 + alpha * (tau_f - 1)) # eq 5.52
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

        return output

    def ideal_turbofan_optimal_fan_pressure_ratio(self,M0, gamma, cp, hpr, Tt4, pi_c, alpha, batch_size=1, min_pi_c=0.001, max_pi_c=40):

        """
        Description: This method calculates the on design parameters of an ideal turbofan engine.

        Arguments:
            M0: Mach number                                             [  -  ]
            gamma: Ratio of specific heats                              [kJ/kgK]
            cp: Specific heat at constant pressure                      [ J/K ]
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
            'Pi_f_optimal': [],
            'tau_f_optimal': []
        }

        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:


            R = (gamma - 1)/gamma * cp # eq padrão
            V0 = self.a0 * M0 # eq padrão
            tau_r = 1 + (gamma - 1)/2 * M0**2 # eq 5.18c
            tau_c = pi_c ** ((gamma - 1) / gamma)  # assumption ideal cycle
            tau_lambda = Tt4/self.T0 # eq 5.58d
            tau_f_opt = ( tau_lambda - tau_r*(tau_c-1) - (tau_lambda/(tau_r*tau_c)) + alpha*tau_r + 1)/ ( tau_r*(alpha+1)) #eq 5.66
            pi_f_optimal = tau_f_opt**(gamma/(gamma-1)) # eq 5.69b
            V19_a0 = ( (2/(gamma -1))*(tau_r*tau_f_opt -1) )**0.5 # eq. 5.69c
            F_m0 = self.a0 * (V19_a0 - M0) #eq. 5.69d
            eta_P =  (2*M0)/(V19_a0 + M0) #eq. 5.69e
            eta_T = 1 - 1 / (tau_r * tau_c)  # eq. 5.22
            f = cp * self.T0 / hpr * (tau_lambda - tau_r * tau_c)  # eq 5.51
            S = f / ((1 + alpha) * F_m0)  # eq 5.54
            eta_Total = eta_P * eta_T # eq 5.58n

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                    eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)
            output['Pi_f_optimal'].append(pi_f_optimal)
            output['tau_f_optimal'].append(tau_f_opt)

            pi_c += pi_c_increase

        return output



    def ideal_turbofan_optimal_bypass_ratio(self,M0, gamma, cp, hpr, Tt4, pi_c, pi_f, batch_size=1, min_pi_c=0.001, max_pi_c=40):
        """
        Description: This method calculates the on design parameters of an ideal turbofan engine.

        Arguments:
            M0: Mach number                                             [  -  ]
            gamma: Ratio of specific heats                              [kJ/kgK]
            cp: Specific heat at constant pressure                      [ J/K ]
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
            'alpha_optimal': []
        }

        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:

            R = (gamma - 1)/gamma * cp  # eq. padrão
            V0 = self.a0 * M0 # eq. padrão
            tau_r = 1 + (gamma - 1)/2 * M0**2 # eq 5.58c
            tau_lambda = Tt4 / self.T0  # eq 5.58d
            tau_c = pi_c ** ((gamma - 1) / gamma)  # eq 5.58e  assumption ideal cycle
            tau_f = pi_f**((gamma - 1)/gamma) # eq 5.58f
            V19_a0 = (2 / (gamma - 1) * (tau_r * tau_f - 1)) ** (1 / 2)  # eq 5.58h

            # optimal bypass for fuel minimization:

            alpha_opt = (1 / (tau_r*(tau_f-1))) * (tau_lambda - tau_r*(tau_c - 1) - (tau_lambda/ (tau_r*tau_c)) - 0.25*( (tau_r*tau_f - 1)**0.5 + (tau_r -1))**2) #eq 5.63a
            F_m0 = self.a0 * ( (1 + 2*alpha_opt)/ 2*(1 + alpha_opt) )  * (( (2/(gamma -1))*(tau_r*tau_f -1) )**0.5 - M0) #eq. 5.63b
            eta_P =  (4*( 1 + 2*alpha_opt)*M0) / ( (3 + 4*alpha_opt)*M0  + (1+ 4*alpha_opt)*V19_a0 ) #eq 5.63c

            # eqs restantes
        
            eta_T = 1 - 1 / (tau_r * tau_c)  # eq 5.58l
            f = cp * self.T0 / hpr * (tau_lambda - tau_r * tau_c)  # eq 5.58j
            S = f / ((1 + alpha_opt) * F_m0)  # eq 5.58k
            eta_Total = eta_P * eta_T # eq 5.58 n

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                    eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)
            output['alpha_optimal'].append(alpha_opt)

            pi_c += pi_c_increase

        return output


    def ideal_turbofan_mixed_flow(self,M0, gamma, cp, hpr, Tt4, Tt7, pi_c, afterburner, alpha = 123456789, pi_f = 123456789, input_choice_case = 0, batch_size=1, min_pi_c=0.001, max_pi_c=40):

        """

        Description: This method calculates the on design parameters of an ideal turbofan engine.

        Arguments:
            M0: Mach number                                             [  -  ]
            gamma: Ratio of specific heats                              [kJ/kgK]
            cp: Specific heat at constant pressure                      [ J/K ]
            hpr: Low heating value of fuel                              [kJ/kg]
            Tt4: Total temperature leaving the burner                   [  K  ]
            Tt4: Total temperature leaving the afterburner              [  K  ]
            pi_c: Compressor total pressure ratio                       [  -  ]
            pi_f: fan total pressure ratio (if chosen)                  [  -  ]
            alpha: bypass ratio  (if chosen)                            [  -  ]
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
            pi_f: fan total pressure ratio (if not chosen as input)
            alpha: bypass ratio  (if not chosen as input)
"""

        #(alpha != 123456 and pi_f == 123456):
        if input_choice_case == 1:
            if pi_f == 123456789:
                output = "in case 1, fan pressure must be provided as input"
            else:
                output = {
                    'pi_c': [],
                    'F_m0': [],
                    'f': [],
                    'S': [],
                    'eta_T': [],
                    'eta_P': [],
                    'eta_Total': [],
                    'alpha': []
                }

        elif input_choice_case == 2:
            if alpha == 123456789:
                output = "in case 2, bypass ratio (alpha) must be provided as input"
            else:
                output = {
                    'pi_c': [],
                    'F_m0': [],
                    'f': [],
                    'S': [],
                    'eta_T': [],
                    'eta_P': [],
                    'eta_Total': [],
                    'pi_f': []
                }
        else:
            output = 'Escolha somente entre input_choice_case = 1 (para o caso de bypass como input) ou input_choice_case = 2 (para o caso de pressure fan como input)  '


        pi_c_increase = 1

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:


            R = (gamma - 1)/gamma * cp  #eq padrão
            V0 = self.a0 * M0 # eq padrão
            tau_r = 1 + (gamma - 1)/2 * M0**2 # eq 5.86c
            tau_lambda = Tt4 / self.T0  # eq 5.86d
            tau_c = pi_c ** ((gamma - 1) / gamma)  # eq 5.86e  assumption ideal cycle

            if input_choice_case == 1: #caso escolhido o pi_f como entrada
                tau_f = pi_f ** ((gamma - 1) / gamma)  # eq 5.86f
                alpha = (tau_lambda*(tau_c - tau_f))/(tau_r*tau_c*(tau_f -1)) -  ((tau_c-1)/(tau_f - 1)) #eq 5.86g
                if alpha < 0:
                    alpha = 0

            elif input_choice_case == 2: #caso escolhido o alpha como entrada

                tau_f = ((tau_lambda/tau_r) - (tau_c - 1) + alpha) / ((tau_lambda / (tau_r*tau_c)) + alpha) #eq 5.86h
                pi_f = tau_f **(gamma/(gamma -1)) #eq 5.86i



            tau_t = 1 - ((tau_r/tau_lambda)*(tau_c - 1 + (alpha*(tau_f - 1)))) #eq 5.86j

            f = cp * self.T0 / hpr * (tau_lambda - tau_r * tau_c)  # eq 5.86k

            tau_m = (1 / (1 + alpha)) * (1 + alpha*((tau_f*tau_r )/ (tau_lambda*tau_t)))   # eq 5.86l

            if afterburner == 1:
                tau_lambda_AB = Tt7/(self.T0)  # eq 5.86 m
                f_AB =  cp * self.T0 / hpr * (tau_lambda_AB - tau_lambda*tau_t*tau_m)  # eq 5.86n
                T9_T0 = tau_lambda_AB / (tau_r*tau_f)  # eq 5.86o


            elif afterburner == 0:
                f_AB = 0 # eq 5.86p
                T9_T0 = (tau_lambda*tau_t*tau_m)/(tau_r*tau_f)  # eq 5.86q


            M9 =  ((2/(gamma - 1)) * (tau_r*tau_f - 1))**0.5  # eq 5.86r
            V9_a0 = (T9_T0**0.5) * M9  # eq 5.86s
            f_overall = f/ (1+alpha) + f_AB  # eq 5.86t

            F_m0 = self.a0 * ( V9_a0 - M0)  # eq 5.86u

            S = f_overall/ F_m0 # eq 5.86v

            eta_T = (gamma - 1)/2 *  ((cp * self.T0)/ (hpr * f_overall))* (V9_a0**2 - M0**2)  # eq 5.86w
            eta_P = (2*M0) / (V9_a0 + M0)  # eq 5.86x
            eta_Total = eta_T*eta_P  # eq 5.86y

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                    eta_T) or math.isnan(eta_Total):
                pi_c += pi_c_increase
                continue


            if input_choice_case == 1:
                output['pi_c'].append(pi_c)
                output['F_m0'].append(F_m0)
                output['f'].append(f)
                output['S'].append(S)
                output['eta_T'].append(eta_T)
                output['eta_P'].append(eta_P)
                output['eta_Total'].append(eta_Total)
                output['alpha'].append(alpha)

            elif input_choice_case == 2:

                output['pi_c'].append(pi_c)
                output['F_m0'].append(F_m0)
                output['f'].append(f)
                output['S'].append(S)
                output['eta_T'].append(eta_T)
                output['eta_P'].append(eta_P)
                output['eta_Total'].append(eta_Total)
                output['pi_f'].append(pi_f)

            pi_c += pi_c_increase

        return output

    def real_turbofan(self,
                          M0,
                          gamma_c,
                          gamma_t,
                          cp_c,
                          cp_t,
                          hpr,
                          Tt4,
                          pi_d_max,
                          pi_b,
                          pi_n,
                          pi_fn,
                          e_cL,
                          e_cH,
                          e_f,
                          e_tL,
                          e_tH,
                          eta_b,
                          eta_mL,
                          eta_mH,
                          P0_P9,
                          P0_P19,
                          tau_n,
                          tau_fn,
                          pi_cL,
                          pi_cH,
                          pi_f,
                          alpha,
                          batch_size=1, min_pi_c=0.001, max_pi_c=40):

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
            'FR': []
        }

        R_c = (gamma_c - 1) / gamma_c * cp_c  # J/(kg.K)
        R_t = (gamma_t - 1) / gamma_t * cp_t  # J/(kg.K)

        a0 = (gamma_c * R_c * self.T0) ** (1 / 2)  # m/s
        V0 = a0 * M0  # m/s

        # Free stream parameters
        tau_r = 1 + (gamma_c - 1) / 2 * M0 ** 2

        pi_r = tau_r ** (gamma_c / (gamma_c - 1))

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075 * (M0 - 1) ** 1.35

        # Diffuser parameters
        pi_d = pi_d_max * eta_r
        tau_d = pi_d ** ((gamma_c - 1) / gamma_c)

        # Fan parameters
        tau_f = pi_f ** ((gamma_c - 1) / (gamma_c * e_f))
        eta_f = (pi_f ** ((gamma_c - 1) / gamma_c) - 1) / (tau_f - 1)

        # Enthalpy
        tau_lambda = cp_t * Tt4 / (cp_c * self.T0)

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

        V9_a0 = M9 * (R_t * gamma_t / (R_c * gamma_c) * T9_T0) ** (1 / 2)

        # Parametros referentes a saida do bypass apos o fan
        Pt19_P19 = P0_P19 * pi_r * pi_d * pi_f * pi_fn

        M19 = (2 / (gamma_c - 1) * (Pt19_P19 ** ((gamma_c - 1) / gamma_c) - 1)) ** (1 / 2)

        Tt19_T0 = tau_r * tau_d * tau_f * tau_fn

        T19_T0 = Tt19_T0 / Pt19_P19 ** ((gamma_c - 1) / gamma_c)

        V19_a0 = M19 * (T19_T0) ** (1 / 2)

        # Engine performance parameters
        FF_m0 = alpha / (1 + alpha) * a0 * (V19_a0 - M0 + T19_T0 / V19_a0 * (1 - P0_P19) / gamma_c)  # N/(kg/s)
        FC_m0 = 1 / (1 + alpha) * a0 * (
                    (1 + f) * V9_a0 - M0 + (1 + f) * R_t / R_c * T9_T0 / V9_a0 * (1 - P0_P9) / gamma_c)  # N/(kg/s)
        F_m0 = FF_m0 + FC_m0  # N/(kg/s)

        S = f / ((1 + alpha) * F_m0)

        FR = FF_m0 / FC_m0

        eta_T = a0 * a0 * ((1 + f) * V9_a0 * V9_a0 + alpha * (V19_a0 * V19_a0) - (1 + alpha) * M0 * M0) / (2 * f * hpr)
        eta_P = 2 * M0 * ((1 + f) * V9_a0 + alpha * V19_a0 - (1 + alpha) * M0) / (
                    (1 + f) * (V9_a0 ** 2) + alpha * V19_a0 ** 2 - (1 + alpha) * M0 ** 2)
        eta_Total = eta_P * eta_T

        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)
        output['FR'].append(FR)

        return output

    def real_turbofan_with_afterburner(self, M0, gamma_c, gamma_t, gamma_AB, gamma_DB, cp_c, cp_t, cp_AB, AB, DB, cp_DB, hpr, Tt4, Tt7,
                      Tt17, pi_d_max, pi_b, pi_M_max, pi_AB, pi_DB, pi_n, pi_fn, e_c, e_f, e_t, eta_b, eta_m, eta_AB,
                      eta_DB, P0_P9, P0_P19, tau_n, tau_fn, pi_c, pi_f,
                      alpha, M6, batch_size=1.1, min_pi_c=0.001, max_pi_c=30):
        """
        Description: This method calculates the on design parameters of a real single spool turbofan engine.

        Arguments:
            AB = if 1, afterburner is on, else, afterburner is off
            DB = if 1, it is turbofan with afterburner - separate exhaust streams
            else, it is turbofan with afterburner - mixed exhaust streams

            M0: Mach number
            gamma_c: Ratio of specific heats at the compressor
            gamma_t: Ratio of specific heats at the turbine
            cp_c: Specific heat at constant pressure at the compressor
            cp_t: Specific heat at constant pressure at the turbine
            hpr: Low heating value of fuel
            Tt4/Tt7: Total temperature leaving the burner
            pi_d_max: Maximum total pressure ratio at the difuser
            pi_DB: Total pressure ratio at the duct burner
            pi_b: Total pressure ratio at the burner
            pi_n: Total pressure ratio at the nozzle
            pi_fn: Total pressure ratio between the fan and the nozzle
            e_c: Politropic efficiency of the compressor
            e_f: Politropic efficiency of the fan
            e_t: Politropic efficiency of the turbine
            eta_b: Burner efficiency
            eta_m: Mechanical efficiency
            P0_P9: Pressure ratio between the freestream and the gas generator outlet
            P0_P19: Pressure ratio between the freestream and the fan outlet
            tau_n: Total temperature ratio at the nozzle
            tau_fn: Total temperature ratio between the fan and the nozzle
            pi_c: Total pressure ratio at the  compressor
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
            pi_c_increase = (max_pi_c - min_pi_c) / batch_size

        while pi_c <= max_pi_c:
            R_c = (gamma_c - 1) / gamma_c * cp_c  # J/(kg.K)
            R_t = (gamma_t - 1) / gamma_t * cp_t  # J/(kg.K)

            a0 = (gamma_c * R_c * self.T0) ** (1 / 2)  # m/s
            V0 = a0 * M0  # m/s

            # Free stream parameters
            tau_r = 1 + (gamma_c - 1) / 2 * M0 ** 2

            pi_r = tau_r ** (gamma_c / (gamma_c - 1))

            if M0 <= 1:
                eta_r = 1
            else:
                eta_r = 1 - 0.075 * (M0 - 1) ** 1.35

            # Diffuser parameters
            pi_d = pi_d_max * eta_r
            tau_d = pi_d ** ((gamma_c - 1) / gamma_c)

            # Fan parameters
            tau_f = pi_f ** ((gamma_c - 1) / (gamma_c * e_f))
            eta_f = (pi_f ** ((gamma_c - 1) / gamma_c) - 1) / (tau_f - 1)

            # Enthalpy
            tau_lambda = cp_t * Tt4 / (cp_c * self.T0)

            # Compressor parameters
            tau_c = pi_c ** ((gamma_c - 1) / (gamma_c * e_c))
            eta_c = (pi_c ** ((gamma_c - 1) / gamma_c) - 1) / (tau_c - 1)

            # Turbine parameters
            f = (tau_lambda - tau_r * tau_c) / (hpr * eta_b / (cp_c * self.T0) - tau_lambda)
            tau_t = 1 - (1 / (eta_m * (1 + f))) * (tau_r / tau_lambda) * (tau_c - 1 + alpha * (tau_f - 1))
            pi_t = tau_t ** (gamma_t / ((gamma_t - 1) * e_c))
            eta_t = (tau_t - 1) / (1 - tau_t ** (1 / e_t))

            if AB == 0 and DB == 1:
                # Turbofan without afterburner = separate exhaust streams
                # Engine core parameters
                Pt9_P9 = P0_P9 * pi_r * pi_d * pi_f * pi_c * pi_b * pi_t * pi_t * pi_n
                M9 = (2 / (gamma_c - 1) * (Pt9_P9 ** ((gamma_c - 1) / gamma_c) - 1)) ** (1 / 2)
                Tt9_T0 = cp_c / cp_t * tau_lambda * tau_t * tau_t * tau_n
                T9_T0 = Tt9_T0 / Pt9_P9 ** ((gamma_t - 1) / gamma_t)
                V9_a0 = M9 * (R_t * gamma_t / (R_c * gamma_c) * T9_T0) ** (1 / 2)

                # Parametros referentes a saida do bypass apos o fan
                Pt19_P19 = P0_P19 * pi_r * pi_d * pi_f * pi_fn
                M19 = (2 / (gamma_c - 1) * (Pt19_P19 ** ((gamma_c - 1) / gamma_c) - 1)) ** (1 / 2)
                Tt19_T0 = tau_r * tau_d * tau_f * tau_fn
                T19_T0 = Tt19_T0 / Pt19_P19 ** ((gamma_c - 1) / gamma_c)
                V19_a0 = M19 * (T19_T0) ** (1 / 2)

                # Engine performance parameters
                FF_m0 = alpha / (1 + alpha) * a0 * (V19_a0 - M0 + T19_T0 / V19_a0 * (1 - P0_P19) / gamma_c)  # N/(kg/s)
                FC_m0 = 1 / (1 + alpha) * a0 * ((1 + f) * V9_a0 - M0 + (1 + f) * R_t / R_c * T9_T0 / V9_a0 * (
                            1 - P0_P9) / gamma_c)  # N/(kg/s)
                F_m0 = FF_m0 + FC_m0  # N/(kg/s)
                S = f / ((1 + alpha) * F_m0)
                FR = FF_m0 / FC_m0
                eta_T = a0 * a0 * ((1 + f) * V9_a0 * V9_a0 + alpha * (V19_a0 * V19_a0) - (1 + alpha) * M0 * M0) / (
                            2 * f * hpr)
                eta_P = 2 * M0 * ((1 + f) * V9_a0 + alpha * V19_a0 - (1 + alpha) * M0) / (
                            (1 + f) * (V9_a0 ** 2) + alpha * V19_a0 ** 2 - (1 + alpha) * M0 ** 2)
                eta_Total = eta_P * eta_T

                if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                        eta_T) or math.isnan(eta_Total):
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

            elif (AB == 1 and DB == 1):
                # Turbofan with afterburner - separate exhaust streams
                # Gas constants
                R_DB = ((gamma_DB - 1) / gamma_DB) * cp_DB
                R_AB = ((gamma_AB - 1) / gamma_AB) * cp_AB

                # Afterburner
                tal_lambda_AB = cp_AB * Tt7 / (cp_c * self.T0)
                f_AB = (1 + f) * (tal_lambda_AB - tau_lambda * tau_t) / (
                            (hpr * eta_AB / (cp_c * self.T0)) - tal_lambda_AB)

                # Ductburner
                tal_lambda_DB = cp_DB * Tt17 / (cp_c * self.T0)
                f_DB = (tal_lambda_DB - tau_r * tau_f) / ((hpr * eta_DB / (cp_c * self.T0)) - tal_lambda_DB)

                # Auxiliar
                Pt9_P9 = (P0_P9) * pi_r * pi_d * pi_c * pi_b * pi_t * pi_n * pi_AB
                T9_T0 = (Tt7 / self.T0) / (((Pt9_P9) ** ((gamma_AB - 1) / gamma_AB)))
                M9 = (2 / (gamma_AB - 1) * (Pt9_P9 ** ((gamma_AB - 1) / gamma_AB) - 1)) ** (1 / 2)
                V9_a0 = M9 * (math.sqrt(gamma_AB * R_AB * (T9_T0) / (gamma_c * R_c)))

                Pt19_P19 = (P0_P19) * pi_r * pi_d * pi_f * pi_DB * pi_fn
                M19 = (2 / (gamma_DB - 1) * (Pt19_P19 ** ((gamma_DB - 1) / gamma_DB) - 1)) ** (1 / 2)
                T19_T0 = (Tt17 / self.T0) / (((Pt19_P19) ** ((gamma_DB - 1) / gamma_DB)))
                V19_a0 = M19 * (math.sqrt(gamma_DB * R_DB * (T19_T0) / (gamma_c * R_c)))

                # Results
                F_m0 = (1 / (1 + alpha)) * a0 * (
                            (1 + f + f_AB) * V9_a0 - M0 + (1 + f + f_AB) * (R_AB * T9_T0 / (R_c * V9_a0)) * (
                                1 - P0_P9) / gamma_c) + (alpha / (1 + alpha)) * a0 * (
                                   (1 + f_DB) * V19_a0 - M0 + (1 + f_DB) * (R_DB * T19_T0 / (R_c * V19_a0)) * (
                                       1 - P0_P19) / gamma_c)
                S = (f + f_AB + alpha * f_DB) / (F_m0 * (1 + alpha))

                if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                        eta_T) or math.isnan(eta_Total):
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
            else:
                # Turbofan with afterburner - Mixed flow: Here, the afterburner can be on or off, but DB =0

                # Gas constants
                R_AB = ((gamma_AB - 1) / gamma_AB) * cp_AB

                # Afterburner
                tal_lambda_AB = cp_AB * Tt7 / (cp_c * self.T0)

                # Turbine
                alpha = (eta_m * (1 + f) * (tau_lambda / tau_r) * (
                            1 - (pi_f / (pi_c * pi_b)) ** ((gamma_t - 1) * (e_t / gamma_t))) - (tau_c - 1)) / (
                                    tau_f - 1)
                tau_t = 1 - (1 / (eta_m * (1 + f))) * (tau_r / tau_lambda) * (tau_c - 1 + alpha * (tau_f - 1))
                pi_t = tau_t ** (gamma_t / ((gamma_t - 1) * e_t))
                eta_t = (1 - tau_t) / (1 - tau_t ** (1 / e_t))

                # Auxiliar
                Pt16_P6 = pi_f / (pi_c * pi_b * pi_t)

                M16 = ((2 / (gamma_c - 1)) * (
                            Pt16_P6 * (1 + (((gamma_t - 1) / 2) * M6 ** 2) ** (gamma_t / (gamma_t - 1))) ** (
                                (gamma_c - 1) / gamma_c)) - 1) ** 0.5
                alpha_line = alpha / (1 + f)

                # Constants of the mixer area
                cp_6A = (cp_t + alpha_line * cp_c) / (1 + alpha_line)
                R_6A = (R_t + alpha_line * R_c) / (1 + alpha_line)
                gamma_6A = cp_6A / (cp_6A - R_6A)

                # Bypass exit
                Tt16_Tt6 = (self.T0 / Tt4) * tau_r * tau_f / tau_t

                # Mixture
                tau_M = (cp_t / cp_6A) * ((1 + alpha_line * ((cp_c / cp_t) * Tt16_Tt6))) / (1 + alpha_line)

                # 16 --> bypass
                # 6A --> mixed streams
                phi_M6_gamma6 = (M6 ** 2) * (1 + ((gamma_t - 1) / 2) * M6 ** 2) / (1 + (gamma_t * M6 ** 2)) ** 2
                phi_M16_gamma16 = (M16 ** 2) * (1 + ((gamma_c - 1) / 2) * M16 ** 2) / (1 + (gamma_c * M16 ** 2)) ** 2
                phi = (((1 + alpha_line) / ((1 / phi_M6_gamma6) + alpha_line * (R_c * (gamma_t / (R_t * gamma_c)) * (
                            Tt16_Tt6 / phi_M16_gamma16)) ** 0.5)) ** 2) * R_6A * gamma_t * tau_M / (R_t * gamma_6A)
                M6A = (2 * phi / (1 - 2 * gamma_6A * phi + (1 - 2 * (gamma_6A + 1)) ** 0.5)) ** 0.5
                A16_A6 = (alpha_line * (Tt16_Tt6) ** 0.5) / ((M16 / M6) * (((gamma_c * R_t / (gamma_t * R_c)) * (
                (1 + ((gamma_c - 1) / 2) * M16 ** 2)) / ((1 + ((gamma_t - 1) / 2) * M6 ** 2))) ** 0.5))

                # Mass Flow Parameter
                MFP_M6_t_rt = M6 / ((gamma_t / R_t) ** 0.5)
                MFP_A = M6A / ((gamma_6A / R_6A) ** 0.5)

                pi_M_ideal = (((1 + alpha_line) * (tau_M) ** 0.5) / (1 + A16_A6)) * (MFP_M6_t_rt / MFP_A)

                pi_M = pi_M_max * pi_M_ideal

                # Auxiliar
                Pt9_P9 = (P0_P9) * pi_r * pi_d * pi_c * pi_b * pi_t * pi_n * pi_AB * pi_M

                # Afterburner on
                if AB == 1:
                    cp9 = cp_AB
                    R9 = R_AB
                    gamma_9 = gamma_AB
                    f_AB = (1 + f / (1 + alpha)) * (tal_lambda_AB - (cp_6A / cp_t) * tau_lambda * tau_t * tau_M) / (
                                ((eta_AB * hpr) / (cp_c * self.T0)) - tal_lambda_AB)
                    T9_T0 = (Tt7 / self.T0) / (Pt9_P9) ** ((gamma_9 - 1) / gamma_9)
                else:  # Afterburner off
                    cp9 = cp_6A
                    R9 = R_6A
                    gamma_9 = gamma_6A
                    f_AB = 0
                    T9_T0 = (Tt4 * tau_t * tau_M / self.T0) / (Pt9_P9) ** ((gamma_9 - 1) / gamma_9)

                # Auxiliar

                M9 = (2 / (gamma_9 - 1) * (Pt9_P9 ** ((gamma_9 - 1) / gamma_9) - 1)) ** (0.5)
                V9_a0 = M9 * (math.sqrt(gamma_9 * R9 * (T9_T0) / (gamma_c * R_c)))

                # Results
                f_0 = (f / (1 + alpha)) + f_AB
                F_m0 = a0 * ((1 + f_0) * V9_a0 - M0 + (1 + f_0) * R9 * T9_T0 / (R_c * V9_a0) * (1 - P0_P9) / gamma_c)
                S = f_0 / F_m0
                eta_T = ((a0 ** 2) * ((1 + f_0) * V9_a0 ** 2 - M0 ** 2) / (2 * (f_0) * (hpr)))
                eta_P = (2 * V0 * F_m0 / ((a0 ** 2) * ((1 + f_0) * V9_a0 ** 2 - M0 ** 2)))
                eta_Total = eta_T * eta_P

                if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(
                        eta_T) or math.isnan(eta_Total):
                    pi_c += pi_c_increase
                    continue

                output['pi_c'].append(pi_c)
                output['F_m0'].append(F_m0)
                output['f'].append(f)
                output['S'].append(S)
                output['eta_T'].append(eta_T)
                output['eta_P'].append(eta_P)
                output['eta_Total'].append(eta_Total)
                # output['FR'].append(FR)

                pi_c += pi_c_increase
        return output


    def real_turbofan_with_AB_mixed_off_design(
            ## Choices ##
            # Flight Parameters
            self,
            M0,

            # Throttle Setting
            Tt4,
            Tt7,

            # Exhaust Nozzle
            P0_P9,

            # Engine control
            TR,

            ## Design Constants ##
            # pressure ratio
            pi_d_max,
            pi_b,
            pi_tH,
            pi_AB,
            pi_n,
            pi_M_max,

            # temperature ratio
            tau_tH,

            # Isentropic Efficiency
            eta_f,
            eta_cH,
            eta_b,
            eta_AB,
            eta_mH,
            eta_mL,

            # Gas Properties
            gamma_c,
            gamma_t,
            gamma_AB,
            cp_c,
            cp_t,
            cp_AB,

            # Fuel
            hpr,

            ## Reference Conditions ##
            # Flight Parameters
            M0_R,
            T0_R,
            P0_R,
            tau_r_R,
            pi_r_R,
            theta0_R,
            m0_R,

            # Throttle Setting
            Tt4_R,
            Tt7_R,

            # Component Behavior
            pi_d_R,
            pi_f_R,
            pi_cH_R,
            pi_tL_R,
            tau_f_R,
            tau_cH_R,
            tau_tL_R,
            alpha_R,
            M6_R,
            M9_R,
            A6_A16
    ):

        # Equations
        R_c = (gamma_c - 1) / gamma_c * cp_c
        R_t = (gamma_t - 1) / gamma_t * cp_t
        R_AB_R = (gamma_AB - 1) / gamma_AB * cp_AB
        a0 = (gamma_c * R_c * self.T0) ** (1 / 2)
        V0 = a0 * M0
        tau_r = 1 + (gamma_c - 1) / 2 * M0 ** 2
        pi_r = tau_r ** (gamma_c / (gamma_c - 1))
        Tt2 = self.T0 * tau_r
        Tt2_R = self.T0 * tau_r_R

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075 * (M0 - 1) ** 1.35

        pi_d = pi_d_max * eta_r

        tau_lambda = cp_t * Tt4 / (cp_c * self.T0)
        tau_lambda_R = cp_t * Tt4_R / (cp_c * self.T0)
        alpha_linha_N = 0
        f_R = (tau_lambda_R - tau_r_R * tau_f_R * tau_cH_R) / (hpr * eta_b / (cp_t * self.T0) - tau_lambda_R)
        alpha_linha_R = alpha_R / (1 + f_R)

        if theta0_R >= TR:
            Tt4_max = Tt4_R
        else:
            Tt4_max = Tt4_R * (TR / theta0_R)

        theta0 = tau_r * self.T0 / T0_R

        if theta0 >= TR:
            Tt4_lim = Tt4_max
        else:
            Tt4_lim = Tt4_max * theta0 / TR

        if TR >= 1 & Tt4 > Tt4_lim:
            Tt4 = Tt4_lim
            alpha_linha = alpha_linha_R
        else:
            alpha_linha = alpha_linha_R * theta0 / theta0_R



        while abs(alpha_linha_N - alpha_linha) > 0.001:
            alpha_linha = alpha_linha_N

            teste = 10

            while teste > 0.0001 or teste < -0.0001:
                if teste == 10:
                    tau_tL = tau_tL_R
                    tau_f = tau_f_R
                    pi_tL = pi_tL_R

                alpha = alpha_R / alpha_linha_R
                tau_f = 1 + ((1 - tau_tL) / (1 - tau_tL_R) * (tau_lambda / tau_r / (tau_lambda_R / tau_r_R)) * (
                        (1 + alpha_R) / (1 + alpha)) * (tau_f_R - 1))
                pi_f = (1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))
                tau_cH = 1 + ((Tt4 / self.T0) / (Tt4_R / T0_R)) * (tau_r_R * tau_f_R / (tau_r * tau_f)) * (tau_cH_R - 1)
                pi_cH = (1 + (tau_cH - 1) * eta_cH) ** (gamma_c / (gamma_c - 1))
                R6 = R_t
                R16 = R_c
                cp6 = cp_t
                cp16 = cp_c
                gamma6 = gamma_t
                gamma16 = gamma_c
                MFP_M6_R = M6_R * (gamma_t / R_t) ** (1 / 2) * (1 + (gamma_t - 1) / 2 * M6_R ** 2) ** (
                        (gamma_t + 1) / (2 * (1 - gamma_t)))
                MFP_M6 = MFP_M6_R * (tau_tL / tau_tL_R) ** (1 / 2) * pi_tL_R / pi_tL

                ## Solving M6

                M6_solve = 0
                MFP = 1

                while abs(MFP - MFP_M6) > 0.5:
                    M6_solve = M6_solve + 0.001
                    MFP = M6_solve * (gamma_t / R_t) ** (1 / 2) * (1 + (gamma_t - 1) / 2 * M6_solve ** 2) ** (
                        (gamma_t + 1) / (2 * (1 - gamma_t)))

                M6 = M6_solve

                Pt16_Pt6_R = pi_f_R / (pi_cH_R * pi_b * pi_tL * pi_tH)
                Pt16_P16 = pi_cH_R * pi_tL_R / (pi_cH * pi_tL) * (Pt16_Pt6_R) * (1 + (gamma6 - 1) / 2 * M6 ** 2) ** (
                        gamma6 / (gamma6 - 1))
                M16 = (2 / (gamma16 - 1) * (Pt16_P16 ** ((gamma16 - 1) / gamma16) - 1)) ** (1 / 2)
                tau_tL_N = Tt2 / Tt4 * tau_f / tau_tH * (
                        A6_A16 * M6 / M16 * alpha_linha) ** 2 * gamma6 / gamma16 * R16 / R6 * (
                                   1 + (gamma6 - 1) / 2 * M6 ** 2) / (1 + (gamma16 - 1) / 2 * M16 ** 2)
                teste = tau_tL_N - tau_tL

                if teste > 0.0001:
                    tau_tL = tau_tL + 0.0001
                elif teste < -0.0001:
                    tau_tL = tau_tL - 0.0001

            cp6A = (cp6 + alpha_linha * cp16) / (1 + alpha_linha)
            R6A = (R6 + alpha_linha * R16) / (1 + alpha_linha)
            gamma6A = cp6A / (cp6A - R6A)
            cp6A_R = (cp6 + alpha_linha_R * cp16) / (1 + alpha_linha_R)
            R6A_R = (R6 + alpha_linha_R * R16) / (1 + alpha_linha_R)
            gamma6A_R = cp6A_R / (cp6A_R - R6A_R)
            Tt16_Tt6 = Tt2 / Tt4 * tau_f / (tau_tH * tau_tL)
            tau_M = cp6 / cp6A * (1 + alpha_linha * (cp16 / cp6) * (Tt16_Tt6)) / (1 + alpha_linha)
            tau_M_R = cp6 / cp6A_R * (1 + alpha_linha_R * (cp16 / cp6) * (Tt16_Tt6)) / (1 + alpha_linha_R)
            phi6 = M6 ** 2 * (1 + (gamma6 - 1) / 2 * M6 ** 2) / (1 + gamma6 * M6 ** 2) ** 2
            phi16 = M16 ** 2 * (1 + (gamma16 - 1) / 2 * M16 ** 2) / (1 + gamma16 * M16 ** 2) ** 2
            PHI = ((1 + alpha_linha) / ((1 / phi6) ** (1 / 2) + alpha_linha * (
                (R16 * gamma6 / (R_t * gamma16) * Tt16_Tt6 / phi16)))) ** 2 * R6A * gamma6 / (R6 * gamma6A) * tau_M
            M6A = (2 * PHI / (1 - 2 * gamma6A * PHI + (1 - 2 * (gamma6A + 1) * PHI))) ** (1 / 2)
            MFP_M6A = M6A * (gamma6A / R6A) ** (1 / 2) * (1 + (gamma6A - 1) / 2 * M6A ** 2) ** (
                    (gamma6A + 1) / (2 * (1 - gamma6A)))
            pi_M_ideal = (1 + alpha_linha) * tau_M ** (1 / 2) / (1 + 1 / A6_A16) * MFP_M6 / MFP_M6A
            pi_M = pi_M_max * pi_M_ideal
            pi_AB_dry = 1 - (1 / 2) * (1 - pi_AB)
            Pt9_P9_dry = P0_P9 * pi_r * pi_d * pi_f * pi_cH * pi_b * pi_tH * pi_tL * pi_M * pi_AB_dry * pi_n

            if Pt9_P9_dry >= ((gamma6A + 1) / 2) ** (gamma6A / (gamma6A - 1)):
                choked = 1
                M8_dry = 1
            else:
                choked = 0
                M8_dry = (2 / (gamma6A - 1) * (Pt9_P9_dry ** ((gamma6A - 1) / gamma6A) - 1)) ** (1 / 2)
                MFP_M8 = M8_dry * (gamma6A / R6A) ** (1 / 2) * (1 + (gamma6A - 1) / 2 * M8_dry ** 2) ** (
                        (gamma6A + 1) / (2 * (1 - gamma6A)))
                MFP_M8_R = M8_dry * (gamma6A_R / R6A_R) ** (1 / 2) * (1 + (gamma6A_R - 1) / 2 * M8_dry ** 2) ** (
                        (gamma6A_R + 1) / (2 * (1 - gamma6A_R)))
                alpha_linha_N = (1 + alpha_linha_R) * (pi_tL * pi_M) / (pi_tL_R * pi_M_ideal) * (
                        (tau_tL_R * tau_M_R) / (tau_tL * tau_M)) ** (1 / 2) * MFP_M8 / MFP_M8_R - 1

        alpha = alpha_R * alpha_linha / alpha_linha_R
        m0 = m0_R * (1 + alpha) / (1 + alpha_R) * self.P0 * pi_r * pi_d * pi_f * pi_cH / (
                P0_R * pi_r_R * pi_d_R * pi_f_R * pi_cH_R) * (Tt4_R / Tt4) ** (1 / 2)
        f = (tau_lambda - tau_r * tau_f * tau_cH) / (hpr * eta_b / (cp_t * self.T0) - tau_lambda)

        Tt5 = tau_tH * tau_tL * Tt4
        Tt3 = tau_f * tau_cH * Tt2
        Tt6 = self.T0 * Tt2 / self.T0 * tau_f * tau_cH * Tt4 / Tt3 * tau_tH * tau_tL * Tt7 / Tt5
        Tt6A = Tt6 * tau_M

        if Tt7 >= Tt7_R:
            x = 1
        else:
            x = (Tt7 - Tt6A) / (Tt7_R - Tt6A)

        cp_AB = cp6A + x * (cp_AB - cp6A)
        R_AB = R6A + x * (R_AB_R - R6A)
        gamma_AB = cp_AB / (cp_AB - R_AB)
        pi_AB = 1 - (1 - x) * (1 - pi_AB_dry)
        tau_lambda_AB = cp_AB * Tt7 / (cp_c * self.T0)
        f_AB = (1 + f / (1 + alpha)) * (tau_lambda_AB - (cp6A / cp_t) * tau_lambda * tau_tH * tau_tL * tau_M) / (
                eta_AB * hpr / (cp_c * self.T0) - tau_lambda_AB)
        f_Total = f / (1 + alpha) + f_AB
        Pt9_P9 = P0_P9 * pi_r * pi_d * pi_f * pi_cH * pi_b * pi_tH * pi_tL * pi_M * pi_AB * pi_n
        M9 = (2 / (gamma_AB - 1) * (Pt9_P9 ** ((gamma_AB - 1) / gamma_AB)) - 1) ** (1 / 2)
        T9_T0 = (Tt7 / self.T0) / (Pt9_P9 ** ((gamma_AB - 1) / gamma_AB))
        V9_a0 = M9 * (gamma_AB * R_AB / (gamma_c * R_c) * T9_T0) ** (1 / 2)
        F_m0 = a0 * ((1 + f_Total) * V9_a0 - M0 + (1 + f_Total) * R_AB * T9_T0 * (1 - P0_P9) / (R_c * V9_a0 * gamma_c))
        S = f_Total / F_m0
        eta_P = 2 * V0 * F_m0 / (a0 ** 2 * ((1 + f_Total) * V9_a0 ** 2 - M0 ** 2))
        eta_T = a0 ** 2 * ((1 + f_Total) * V9_a0 ** 2 - M0 ** 2) / (2 * f_Total * hpr)
        eta_Total = eta_P * eta_T
        mc2_mc2_R = (1 + alpha) / (1 + alpha_R) * pi_f * pi_cH / (pi_f_R * pi_cH_R) * (
                (Tt4_R / Tt2_R) / (Tt4 / Tt2)) ** (1 / 2)
        N_NR_L = ((self.T0 * tau_r) / (T0_R * tau_r_R) * (pi_f ** ((gamma_c - 1) / gamma_c) - 1) / (
                pi_f_R ** ((gamma_c - 1) / gamma_c))) ** (1 / 2)
        N_NR_H = ((self.T0 * tau_r * pi_f) / (T0_R * tau_r_R * pi_f_R) * (pi_cH ** ((gamma_c - 1) / gamma_c) - 1) / (
                pi_cH_R ** ((gamma_c - 1) / gamma_c))) ** (1 / 2)

        if choked == 1:
            A9_A8 = gamma_AB / pi_n * ((gamma_AB - 1) / (2 * gamma_AB)) ** (1 / 2) * Pt9_P9 ** (
                    (gamma_AB + 1) / (2 * gamma_AB)) / (Pt9_P9 ** ((gamma_AB + 1) / gamma_AB) - 1) ** (1 / 2)
        else:
            A9_A8 = 1 / pi_n

        output = {
            'F_mo': [F_m0],
            'f': [f_Total],
            'S': [S],
            'eta_T': [eta_T],
            'eta_P': [eta_P],
            'eta_Total': [eta_Total],
            'alpha': [alpha],
            'pi_d': [pi_d],
            'pi_f': [pi_f],
            'pi_cH': [pi_cH],
            'pi_tL': [pi_tL],
            'tau_f': [tau_f],
            'tau_cH': [tau_cH],
            'tau_tL': [tau_tL],
            'f': [f],
            'f_AB': [f_AB],
            'M9': [M9],
            'N_LP_spool': [N_NR_L],
            'N_HP_spool': [N_NR_H],
            'A9_A8': [A9_A8]
        }

        return output

    def real_turbofan_off_design(self,
        M0,
        gamma_c,
        gamma_t,
        cp_c,
        cp_t,
        hpr,
        Tt4,
        pi_d_max,
        pi_b,
        pi_c,
        pi_tH,
        pi_n,
        pi_fn,
        tau_tH,
        eta_f,
        eta_cL,
        eta_cH,
        eta_b,
        eta_mL,
        eta_mH,
        eta_tL,

        # On-design references
        M0_R,
        T0_R,
        P0_R,
        tau_r_R,
        tau_lambda_R,
        pi_r_R,
        Tt4_R,
        pi_d_R,
        pi_f_R,
        pi_cH_R,
        pi_cL_R,
        pi_tL_R,
        tau_f_R,
        tau_tL_R,
        alpha_R,
        M9_R,
        M19_R,
        m0_R
        ):

        tau_cH_R = pi_cH_R**((gamma_c - 1)/(gamma_c))
        tau_cL_R = pi_cL_R**((gamma_c - 1)/(gamma_c))

        R_c = (gamma_c - 1)/gamma_c*cp_c
        R_t = (gamma_t - 1)/gamma_t*cp_t
        a0 = (gamma_c*R_c*self.T0)**(1/2)
        V0 = a0*M0
        tau_r = 1 + (gamma_c - 1)/2*M0**2
        pi_r = tau_r**(gamma_c/(gamma_c - 1))

        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = 1 - 0.075*(M0 - 1)**1.35

        pi_d = pi_d_max*eta_r
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
        T9_T0 = tau_lambda*tau_tH*tau_tL/(Pt9_P9**((gamma_t - 1)/gamma_t))*cp_c/cp_t
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
        eta_T = a0**2*((1 + f)*V9_a0**2 + alpha*(V19_a0**2)- (1 + alpha)*M0**2)/(2*f*hpr)
        eta_P = 2*V0*(1 + alpha)*F_m0/(a0**2*((1 + f)*V9_a0**2 + alpha*V19_a0**2 - (1 + alpha)*M0**2))
        eta_Total = eta_P*eta_T
        F = F_m0 * m0
        mf = S*F
        AF = 1/f
        mC = m0*1/(1 + alpha)
        mF = m0*alpha/(1 + alpha)

        output = {
            'F': [F],
            'm0': [m0],
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
            'N_hp_spool': [N_NR_H]
        }

        return output


#------------------------- RAMJET -------------------------------------------------------
    def ideal_ramjet(self, M0, gamma, cp, hpr, Tt4):
        """
        Description: This method calculates the on design parameters of an ramjet turbojet engine.

        Arguments:
            M0: Mach number                             [  -  ]
            gamma: Ratio of specific heats              [  -  ]
            cp: Specific heat at constant pressure      [J/kgK]
            hpr: Low heating value of fuel              [ J/kg]
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
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            #'FR': []
        }

        R = (gamma - 1)/gamma*cp # J/(kg.K)

        a0 = (gamma*R*self.T0)**(1/2) #m/s
        
        tau_r = 1 + ((gamma - 1)/2)*(M0**2)

        tau_lambda = Tt4/self.T0
        V9_a0 = M0 * ((tau_lambda/tau_r)**0.5)

        F_m0 = a0 * (V9_a0 - M0)
        f = (cp * self.T0)/hpr * (tau_lambda - tau_r)
        S = f/F_m0

        eta_T = 1 - 1/(tau_r)
        eta_P = 2/((tau_lambda/tau_r)**0.5 + 1)
        eta_Total = eta_P*eta_T

        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output

    def real_ramjet(self, M0, gamma_c, gamma_t, cpc, cpt, hpr, Tt4, pi_b, eta_b, pi_dmax, pi_n):
        """
        Description: This method calculates the on design parameters of an ramjet turbojet engine.

        Arguments:
            M0: Mach number                             [  -  ]
            gamma: Ratio of specific heats              [  -  ]
            cp: Specific heat at constant pressure      [J/kgK]
            hpr: Low heating value of fuel              [ J/kg]
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
            'f': [],
            'S': [],
            'eta_T': [],
            'eta_P': [],
            'eta_Total': [],
            #'FR': []
        }
        
        
        R_c = (gamma_c - 1)/gamma_c*cpc # J/(kg.K)
        R_t = (gamma_t - 1)/gamma_t*cpt

        a0 = (gamma_c*R_c*self.T0)**(1/2) #m/s
        V0 = a0*M0
        
        tau_r = 1 + ((gamma_c - 1)/2)*(M0**2)
        pi_r  = tau_r**(gamma_c/(gamma_c-1))
        
        if M0 <= 1:
            eta_r = 1
        else:
            eta_r = (1 - 0.075*(M0-1)**1.35)
            
        pi_d = eta_r*pi_dmax
        tau_d = pi_d**((gamma_c-1)/gamma_c)
        
        tau_lambda = cpt*Tt4/(self.T0*cpc)
        
        tau_n = 1
        
        tau_b = Tt4/(self.T0*tau_d*tau_r)
        
        Pt9_P9 = pi_r*pi_d*pi_b*pi_n
        Pt9 = self.P0*pi_r*pi_d*pi_b*pi_n
        
        P9 = Pt9/Pt9_P9
        
        Tt9 = self.T0*tau_r*tau_d*tau_b*tau_n
        
        T9 = Tt9/(Pt9_P9**((gamma_t-1)/gamma_t))
        
        V9 = a0*(gamma_t*R_t*T9/(gamma_c*R_c*self.T0))
        
        f = (tau_lambda - tau_r*tau_d)/(eta_b*hpr/(cpc*self.T0) - tau_lambda + tau_r*tau_d)
        F_m0 = a0*((1+f)*V9/a0 - M0 + (1+f)*R_t*T9/self.T0*(1-self.P0/P9)/(R_c*V9/a0*gamma_c))
        S = f/F_m0

        eta_T = a0**2*((1+f)*(V9/a0)**2 - M0**2)/(2*f*hpr)
        eta_P = 2*V0*F_m0/(a0**2*((1+f)*(V9/a0)**2)-M0**2)
        eta_Total = eta_P*eta_T

        output['F_m0'].append(F_m0)
        output['f'].append(f)
        output['S'].append(S)
        output['eta_T'].append(eta_T)
        output['eta_P'].append(eta_P)
        output['eta_Total'].append(eta_Total)

        return output



#-------------------------------------------- TURBOPROP --------------------------------------------------
    def ideal_turboprop(self, M0, gamma, cp, hpr, Tt4, pi_c, tau_t, eta_prop, batch_size=1, min_pi_c=0.001, max_pi_c=40):

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
        'C_Total': []
        }

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c)/batch_size

        while pi_c <= max_pi_c:

            R = (gamma - 1)/gamma*cp
            a0 = (gamma*R*self.T0)**(1/2)
            V0 = a0*M0 #m/s
            tau_r = 1 + (gamma - 1)/2*M0**2
            pi_r = tau_r**(gamma/(gamma - 1))
            tau_lambda = Tt4/self.T0
            tau_c = pi_c**((gamma - 1)/(gamma))
            f = cp*self.T0*(tau_lambda - tau_r*tau_c)/hpr
            tau_tH = 1 - tau_r/tau_lambda*(tau_c - 1)
            pi_tH = tau_tH**(gamma/(gamma - 1))
            tau_tL = tau_t/tau_tH
            V9_a0 = np.sqrt(2/(gamma - 1)*(tau_lambda*tau_t - tau_lambda/(tau_r*tau_c)))
            C_c = (gamma - 1)*M0*(V9_a0 - M0)
            C_prop = eta_prop*tau_lambda*tau_tH*(1 - tau_tL)
            C_Total = C_prop + C_c
            F_m0 = C_Total*cp*self.T0/(M0*a0)
            S = f/F_m0
            S_P = f/(C_Total*cp*self.T0)
            eta_T = 1 - 1/(tau_lambda*tau_c)
            eta_Total = C_Total/(tau_lambda - tau_r*tau_c)
            eta_P = eta_Total/eta_T
            AF = 1/f

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(eta_T) or math.isnan(eta_Total) or math.isnan(C_c) or math.isnan(C_prop) or math.isnan(C_Total):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)
            output['C_c'].append(C_c)
            output['C_prop'].append(C_prop)
            output['C_Total'].append(C_Total)

            pi_c += pi_c_increase

        return output

    def real_turboprop(self, M0, T0, gamma_c, gamma_t, cp_c, cp_t, hpr, pi_d_max, pi_b, pi_n, e_c, e_tL, e_tH, eta_b, eta_g, eta_mL, eta_mH, eta_prop, Tt4, pi_c, tau_t, batch_size=1, min_pi_c=0.001, max_pi_c=40):

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
        'C_Total': [],
        'W_m0': [],
        'S_P': []
        }

        if batch_size <= 0:
            return output
        elif batch_size == 1:
            max_pi_c = pi_c
        else:
            pi_c = min_pi_c
            pi_c_increase = (max_pi_c - min_pi_c)/batch_size

        while pi_c <= max_pi_c:

            R_c = (gamma_c - 1)/gamma_c*cp_c
            R_t = (gamma_t - 1)/gamma_t*cp_t
            a0 = (gamma_c*R_c*self.T0)**(1/2)
            V0 = a0*M0
            tau_r = 1 + (gamma_c - 1)/2*M0**2
            pi_r = tau_r**(gamma_c/(gamma_c - 1))
            if M0 <= 1:
                eta_r = 1
            else:
                eta_r = 1 - 0.075*(M0 - 1)**1.35
            pi_d = pi_d_max*eta_r
            tau_lambda = cp_t*Tt4/(cp_c*self.T0)
            tau_c = pi_c**((gamma_c - 1)/(gamma_c*e_c))
            eta_c = (pi_c**((gamma_c - 1)/gamma_c) - 1)/(tau_c - 1)
            f = (tau_lambda - tau_r*tau_c)/(hpr*eta_b/(cp_c*self.T0) - tau_lambda)
            tau_tH = 1 - tau_r*(tau_c - 1)/(eta_mH*(1 + f)*tau_lambda)
            pi_tH = tau_tH**(gamma_t/((gamma_t - 1)*e_tH))
            eta_tH = (1 - tau_tH)/(1 - tau_tH**(1/e_tH))

            tau_tL = tau_t/tau_tH
            C_prop = eta_prop*eta_g*eta_mL*(1 + f)*tau_lambda*tau_tH*(1 - tau_tL)

            pi_tL = tau_tL**(gamma_t/((gamma_t - 1)*e_tL))
            eta_tL = (1 - tau_tL)/(1 - tau_tL**(1/e_tL))
            Pt9_P0 = pi_r*pi_d*pi_c*pi_b*pi_tH*pi_tL*pi_n
            if Pt9_P0 > ((gamma_t + 1)/2)**(gamma_t/(gamma_t - 1)):
                M9 = 1
                Pt9_P9 = ((gamma_t + 1)/2)**(gamma_t/(gamma_t - 1))
                P0_P9 = Pt9_P9/Pt9_P0
            else:
                P0_P9 = 1
                Pt9_P9 = Pt9_P0
                M9 = (2/(gamma_t - 1)*(Pt9_P0**((gamma_t - 1)/gamma_t) - 1))**(1/2)
            V9_a0 = math.sqrt(2*tau_lambda*tau_tH*tau_tL/(gamma_c - 1)*(1 - (Pt9_P9)**(-1*(gamma_t - 1)/gamma_t)))
            Tt9_T0 = tau_lambda*tau_tH*tau_tL
            T9_T0 = Tt9_T0/(Pt9_P9**((gamma_t - 1)/gamma_t))
            C_c = (gamma_c - 1)*M0*((1 + f)*V9_a0 - M0 + (1 + f)*R_t/R_c*T9_T0/V9_a0*(1 - P0_P9)/gamma_c)
            C_Total = C_prop + C_c
            F_m0 = C_Total*cp_c*self.T0/V0
            S = f/F_m0
            S_P = f/(C_Total*cp_c*self.T0)


            W_m0 = C_Total*cp_c*self.T0

            eta_P = C_Total/(C_prop/eta_prop + ((gamma_c - 1)/2)*((1 + f)*V9_a0**2 - M0**2))
            eta_T = C_Total*cp_c*self.T0/(f*hpr)
            eta_Total = eta_P*eta_T
            AF = 1/f

            if math.isnan(F_m0) or math.isnan(S) or math.isnan(f) or math.isnan(eta_P) or math.isnan(eta_T) or math.isnan(eta_Total) or math.isnan(C_c) or math.isnan(C_prop) or math.isnan(C_Total) or math.isnan(W_m0) or math.isnan(S_P):
                pi_c += pi_c_increase
                continue

            output['pi_c'].append(pi_c)
            output['F_m0'].append(F_m0)
            output['f'].append(f)
            output['S'].append(S)
            output['eta_T'].append(eta_T)
            output['eta_P'].append(eta_P)
            output['eta_Total'].append(eta_Total)
            output['C_c'].append(C_c)
            output['C_prop'].append(C_prop)
            output['C_Total'].append(C_Total)
            output['W_m0'].append(W_m0)
            output['S_P'].append(S_P)

            pi_c += pi_c_increase

        return output
