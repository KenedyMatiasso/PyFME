# -*- coding: utf-8 -*-
"""
Python Flight Mechanics Engine (PyFME).
Copyright (c) AeroPython Development Team.
Distributed under the terms of the MIT License.

Cessna 172
----------

    CD - drag coefficient as function of the angle of attack via [2]
    CD_delta_elev - incremental induced-drag coefficient as function of
                    the angle of attack and deflection angle via [2]

    CLsus - lift coefficient as a function of the angle of attack via [2]
    CLsus_alphadot - lift coefficient derivative with respect to the angle of 
                     attack acceleration as function of the angle of attack via [2]
    CLsus_q - lift coefficient derivative with respect to the pitch rate via [2]
    CLsus_delta_elev - lift coefficient derivative with respect to the elevator 
                       deflection as function of the angle of attack via [2]

    CY_beta - side force coefficient derivative with respect to the angle of 
              sideslip via [2]
    CY_p - side force coefficient derivative with respect to the roll rate as 
           function of the angle of attack via [2]
    CY_r - side force coefficient derivative with respect to the yaw rate as
           function of the angle of attack via [1]
    CY_delta_rud - side force coefficient derivative with respect to the rudder
                   deflection via [1]

    Cl_beta - rolling moment coefficient derivative with respect to the sideslip
              angle as function of the angle of attack via [2]
    Cl_p - rolling moment coefficient derivative with respect to the roll rate as
           function of the angle of attack via [2]
    Cl_r - rolling moment coefficient derivative with respect to the yaw rate as
           function of the angle of attack via [2]
    Cl_delta_rud - rolling moment coefficient derivative with respect to the rudder
                   deflection as function of the angle of attack via [1]
    Cl_delta_aile - incremental rolling moment coefficient derivative with respect to 
                    the aileron deflection as function of the aileron deflection via [2]

    CM - pitching moment coefficient derivative with respect to the angle of attack
         as function of the angle of attack via [2]
    CM_q - pitching moment coefficient derivative with respect to the pitch rate via [2]
    CM_alphadot - pitching moment coefficient derivative with respect to the acceleration 
                  of the angle of attack as function of the angle of attack via [2]
    CM_delta_elev - pitching moment coefficient derivative with respect to the elevator 
                    deflection as function of the elevator deflection via [2]

    CN_beta - yawing moment coefficient derivative with respect to the sideslip angle via [2]
    CN_p - yawing moment coefficient derivative with respect to the roll rate as a function
           of the angle of attack via [2]
    CN_r - yawing moment coefficient derivative with respect to the ywa rate as a function of
           the angle of attack via [2]
    CN_delta_rud - yawing moment coefficient derivative with respect to the rudder deflection 
                   as function of the angle of attack via [1]
    CN_delta_aile - incremental yawing moment coefficient derivative with respect to the 
                    aileron deflection as a function of the aileron deflection and the angle 
                    of attack via [2]

References
----------

    [1] ROSKAM, J., Methods for Estimating Stability and Control Derivatives of Conventional Subsonic Airplanes
    [2] McDonnell Douglas Co., The USAF and Stability and Control Digital DATCOM, Users Manual

"""
import numpy as np
from scipy import interpolate

from pyfme.aircrafts.aircraft import Aircraft
from pyfme.models.constants import ft2m, slugft2_2_kgm2, lbs2kg
from pyfme.utils.coordinates import wind2body


class Cessna172(Aircraft):
    """
    Cessna 172

    The Cessna 172 is a blablabla...

    """

    def __init__(self):

        # Mass & Inertia
        self.mass = 2300 * lbs2kg   # kg
        self.inertia = np.diag([948, 1346, 1967]) * slugft2_2_kgm2  # kg·m²
        # Ixz_b = 0 * slugft2_2_kgm2  # Kg * m2

        # Geometry
        self.Sw = 174 * ft2m**2  # m2
        self.chord = 4.9 * ft2m  # m
        self.span = 35.8 * ft2m  # m

        # Aerodynamic Data
        self.alpha_data = np.array([-7.5,-5,-2.5,0,2.5,5,7.5,10,15,17,18,19.5]) # degree
        self.delta_elev_data = np.array([-26,-20,-10,-5,0,7.5,15,22.5,28]) # degree
        self.delta_aile_data = np.array([-15,-10,-5,-2.5,0,5,10,15,20]) # degree

        self.CD_data = np.array([0.044,0.034,0.03,0.03,0.036,0.048,0.067,0.093,0.15,0.169,0.177,0.184])
        self.CD_delta_elev_data = np.array([[0.0135,0.0119,0.0102,0.00846,0.0067,0.0049,0.00309,0.00117,-0.0033,-0.00541,-0.00656,-0.00838],
        [0.0121,0.0106,0.00902,0.00738,0.00574,0.00406,0.00238,0.00059,-0.00358,-0.00555,-0.00661,-0.00831],
        [0.00651,0.00552,0.00447,0.00338,0.00229,0.00117,0.0000517,-0.00114,-0.00391,-0.00522,-0.00593,-0.00706],
        [0.00249,0.002,0.00147,0.000931,0.000384,-0.000174,-0.000735,-0.00133,-0.00272,-0.00337,-0.00373,-0.00429],
        [0,0,0,0,0,0,0,0,0,0,0,0],
        [-0.00089,-0.00015,0.00064,0.00146,0.00228,0.00311,0.00395,0.00485,0.00693,0.00791,0.00844,0.00929],
        [0.00121,0.00261,0.00411,0.00566,0.00721,0.00879,0.0104,0.0121,0.016,0.0179,0.0189,0.0205],
        [0.00174,0.00323,0.00483,0.00648,0.00814,0.00983,0.0115,0.0133,0.0175,0.0195,0.0206,0.0223],
        [0.00273,0.00438,0.00614,0.00796,0.0098,0.0117,0.0135,0.0155,0.0202,0.0224,0.0236,0.0255]])

        self.CL_data = np.array([-0.571,-0.321,-0.083,0.148,0.392,0.65,0.918,1.195,1.659,1.789,1.84,1.889])
        self.CL_alphadot_data = np.array([2.434,2.362,2.253,2.209,2.178,2.149,2.069,1.855,1.185,0.8333,0.6394,0.4971])
        self.CL_q_data = np.array([7.282,7.282,7.282,7.282,7.282,7.282,7.282,7.282,7.282,7.282,7.282,7.282])
        self.CL_delta_elev_data = np.array([-0.132,-0.123,-0.082,-0.041,0,0.061,0.116,0.124,0.137])

        self.CY_beta_data = np.array([-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268,-0.268])
        self.CY_p_data = np.array([-0.032,-0.0372,-0.0418,-0.0463,-0.051,-0.0563,-0.0617,-0.068,-0.0783,-0.0812,-0.0824,-0.083])
        self.CY_r_data = np.array([0.2018,0.2054,0.2087,0.2115,0.2139,0.2159,0.2175,0.2187,0.2198,0.2198,0.2196,0.2194])
        self.CY_delta_rud_data = (-1)*np.array([0.561,0.561,0.561,0.561,0.561,0.561,0.561,0.561,0.561,0.561,0.561,0.561])

        self.Cl_beta_data = np.array([-0.178,-0.186,-0.1943,-0.202,-0.2103,-0.219,-0.2283,-0.2376,-0.2516,-0.255,-0.256,-0.257])
        self.Cl_p_data = np.array([-0.4968,-0.4678,-0.4489,-0.4595,0.487,-0.5085,-0.5231,-0.4916,-0.301,-0.203,-0.1498,-0.0671])
        self.Cl_r_data = np.array([-0.09675,-0.05245,-0.01087,0.02986,0.07342,0.1193,0.1667,0.2152,0.2909,0.3086,0.3146,0.3197])
        self.Cl_delta_rud_data = (-1)*np.array([0.091,0.082,0.072,0.063,0.053,0.0432,0.0333,0.0233,0.0033,-0.005,-0.009,-0.015])
        self.Cl_delta_aile_data = np.array([-0.078052,-0.059926,-0.036422,-0.018211,0,0.018211,0.036422,0.059926,0.078052])

        self.CM_data = np.array([0.0597,0.0498,0.0314,0.0075,-0.0248,0.068,-0.1227,-0.1927,-0.3779,-0.4605,-0.5043,-0.5496,])
        self.CM_q_data = np.array([-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232,-6.232])
        self.CM_alphadot_data = np.array([-6.64,-6.441,-6.146,-6.025,-5.942,-5.861,-5.644,-5.059,-3.233,-2.273,-1.744,-1.356])
        self.CM_delta_elev_data = np.array([0.3302,0.3065,0.2014,0.1007,-0.0002,-0.1511,-0.2863,-0.3109,-0.345])

        self.CN_beta_data = np.array([0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126,0.0126])
        self.CN_p_data = np.array([0.03,0.016,0.00262,-0.0108,-0.0245,-0.0385,-0.0528,-0.0708,-0.113,-0.1284,-0.1356,-0.1422])
        self.CN_r_data = np.array([-0.028,-0.027,-0.027,-0.0275,-0.0293,-0.0325,-0.037,-0.043,-0.05484,-0.058,-0.0592,-0.06015])
        self.CN_delta_rud_data = (-1)*np.array([-0.211,-0.215,-0.218,-0.22,-0.224,-0.226,-0.228,-0.229,-0.23,-0.23,-0.23,-0.23])
        self.CN_delta_aile_data = np.array([[-0.004321,-0.002238,-0.0002783,0.001645,0.003699,0.005861,0.008099,0.01038,0.01397,0.01483,0.01512,0.01539],
        [-0.003318,-0.001718,-0.0002137,0.001263,0.00284,0.0045,0.006218,0.00797,0.01072,0.01138,0.01161,0.01181],
        [-0.002016,-0.001044,-0.000123,0.0007675,0.00173,0.002735,0.0038,0.004844,0.00652,0.00692,0.00706,0.0072],
        [-0.00101,-0.000522,-0.0000649,0.000384,0.000863,0.00137,0.0019,0.00242,0.00326,0.00346,0.00353,0.0036],
        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
        [0.00101,0.00052,0.000065,-0.000384,-0.00086,-0.0014,-0.002,-0.002422,-0.00326,-0.00346,-0.00353,-0.0036],
        [0.00202,0.001044,0.00013,-0.0008,-0.00173,-0.002735,-0.0038,-0.004844,-0.00652,-0.00692,-0.00706,-0.0072],
        [0.00332,0.00172,0.000214,-0.001263,-0.00284,-0.0045,-0.00622,-0.008,-0.01072,-0.01138,-0.01161,-0.01181],
        [0.004321,0.00224,0.00028,-0.001645,-0.0037,-0.00586,-0.0081,-0.0104,-0.014,-0.01483,-0.01512,-0.0154]])

        # CONTROLS
        self.controls = {'delta_elevator': 0,
                         'delta_aileron': 0,
                         'delta_rudder': 0}

        # FIXME: these limits are not real
        self.control_limits = {'delta_elevator': (np.deg2rad(-26), np.deg2rad(28)),  # rad
                               'delta_aileron': (np.deg2rad(-15), np.deg2rad(20)),  # rad
                               'delta_rudder': (np.deg2rad(-16), np.deg2rad(16)),
                               'delta_t': (0, 1)}  # rad

        # Coefficients
        # Aero
        self.CL, self.CD, self.Cm = 0, 0, 0
        self.CY, self.Cl, self.Cn = 0, 0, 0
        # Thrust
        self.Ct = 0

        self.gravity_force = np.zeros(3)
        self.total_forces = np.zeros(3)
        self.total_moments = np.zeros(3)
        self.load_factor = 0

        # Velocities
        self.TAS = 0  # True Air Speed.
        self.CAS = 0  # Calibrated Air Speed.
        self.EAS = 0  # Equivalent Air Speed.
        self.Mach = 0  # Mach number

        self.q_inf = 0  # Dynamic pressure at infty (Pa)

        # Angular velocities
        self.p = 0 # rad/s
        self.q = 0 # rad/s
        self.r = 0 # rad/s

        # Angles
        self.alpha = 0  # rad
        self.beta = 0  # rad
        self.alpha_dot = 0  # rad/s

    def _calculate_aero_lon_forces_moments_coeffs(self):
        delta_elev = np.rad2deg(self.controls['delta_elevator']) # deg
        alpha_DEG = np.rad2deg(self.alpha) # deg
        c = self.chord # m
        V = self.TAS # m/s
        p, q, r = self.p, self.q, self.r # rad/s

        CD_interp = np.interp(alpha_DEG, self.alpha_data, self.CD_data)
        CD_delta_elev_interp = interpolate.RectBivariateSpline(self.delta_elev_data, self.alpha_data, self.CD_delta_elev_data)

        CL_interp = np.interp(alpha_DEG, self.alpha_data, self.CL_data)
        CL_alphadot_interp = np.interp(alpha_DEG, self.alpha_data, self.CL_alphadot_data)
        CL_q_interp = np.interp(alpha_DEG, self.alpha_data, self.CL_q_data)
        CL_delta_elev_interp = np.interp(delta_elev, self.delta_elev_data, self.CL_delta_elev_data)

        CM_interp = np.interp(alpha_DEG, self.alpha_data, self.CM_data)
        CM_q_interp = np.interp(alpha_DEG, self.alpha_data, self.CM_q_data)
        CM_alphadot_interp = np.interp(alpha_DEG, self.alpha_data, self.CM_alphadot_data)
        CM_delta_elev_interp = np.interp(delta_elev, self.delta_elev_data, self.CM_delta_elev_data)

        self.CL = CL_interp + CL_delta_elev_interp + (c/(2 * V)) * (CL_alphadot_interp * self.alpha_dot + CL_q_interp * q) 
        self.CD = CD_interp + CD_delta_elev_interp(delta_elev, alpha_DEG)[0,0] 
        self.CM = CM_interp + CM_delta_elev_interp + (c/(2 * V)) * (CM_q_interp * q + CM_alphadot_interp * self.alpha_dot)

    def _calculate_aero_lat_forces_moments_coeffs(self):
        delta_aile = np.rad2deg(self.controls['delta_aileron']) # deg
        delta_rud = np.rad2deg(self.controls['delta_rudder']) # deg
        delta_rud_RAD = self.controls['delta_rudder'] # rad
        alpha_DEG = np.rad2deg(self.alpha) # deg
        b = self.span
        V = self.TAS
        p, q, r = self.p, self.q, self.r

        CY_beta_interp = np.interp(alpha_DEG, self.alpha_data, self.CY_beta_data)
        CY_p_interp = np.interp(alpha_DEG, self.alpha_data, self.CY_p_data)
        CY_r_interp = np.interp(alpha_DEG, self.alpha_data, self.CY_r_data)
        CY_delta_rud_interp = np.interp(alpha_DEG, self.alpha_data, self.CY_delta_rud_data)

        Cl_beta_interp = np.interp(alpha_DEG, self.alpha_data, self.Cl_beta_data)
        Cl_p_interp = np.interp(alpha_DEG, self.alpha_data, self.Cl_p_data)
        Cl_r_interp = np.interp(alpha_DEG, self.alpha_data, self.Cl_r_data)
        Cl_delta_rud_interp = np.interp(alpha_DEG, self.alpha_data, self.Cl_delta_rud_data)
        Cl_delta_aile_interp = np.interp(delta_aile, self.delta_aile_data, self.Cl_delta_aile_data)

        CN_beta_interp = np.interp(alpha_DEG, self.alpha_data, self.CN_beta_data)
        CN_p_interp = np.interp(alpha_DEG, self.alpha_data, self.CN_p_data)
        CN_r_interp = np.interp(alpha_DEG, self.alpha_data, self.CN_r_data)
        CN_delta_rud_interp = np.interp(alpha_DEG, self.alpha_data, self.CN_delta_rud_data)
        CN_delta_aile_interp = interpolate.RectBivariateSpline(self.delta_aile_data, self.alpha_data, self.CN_delta_aile_data)

        self.CY = CY_beta_interp * self.beta + CY_delta_rud_interp * delta_rud_RAD + (b/(2 * V)) * (CY_p_interp * p + CY_r_interp * r)
        self.Cl = Cl_beta_interp * self.beta + Cl_delta_aile_interp + Cl_delta_rud_interp * delta_rud_RAD + (b/(2 * V)) * (Cl_p_interp * p + Cl_r_interp * r)
        self.CN = CN_beta_interp * self.beta + CN_delta_aile_interp(delta_aile, alpha_DEG)[0,0] + CN_delta_rud_interp * delta_rud_RAD + (b/(2 * V)) * (CN_p_interp * p + CN_r_interp * r)

    def _calculate_aero_forces_moments(self):
        q = self.q_inf
        Sw = self.Sw
        c = self.chord
        b = self.span
        self._calculate_aero_lon_forces_moments_coeffs()
        self._calculate_aero_lat_forces_moments_coeffs()
        L = q * Sw * self.CL
        D = q * Sw * self.CD
        Y = q * Sw * self.CY
        l = q * Sw * b * self.Cl
        m = q * Sw * c * self.CM
        n = q * Sw * b * self.CN
        return L, D, Y, l, m , n

    def _calculate_thrust_forces_moments(self):
        q = self.q_inf
        Sw = self.Sw
        self.Ct = 0.031 * self.controls['delta_t']
        Ft = np.array([q * Sw * self.Ct, 0, 0])
        return Ft


    def calculate_forces_and_moments(self):

        Ft = self._calculate_thrust_forces_moments()
        L, D, Y, l, m, n = self._calculate_aero_forces_moments()
        Fg = self.gravity_force
        # FIXME: is it necessary to use wind2body conversion?
        Fa = np.array([-D, Y, -L])

        self.total_forces = 10 * Ft + Fg + Fa
        self.total_moments = np.array([l, m, n])
        return self.total_forces, self.total_moments
