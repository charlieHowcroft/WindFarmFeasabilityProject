"""To calculate the line parameters of a transmission line"""
import cmath
import numpy as np
import math
import csv

"""Dictionary keys"""
# for conductors
CONDUCTOR_TYPE_KEY = "CONDUCTOR_TYPE_KEY"
DIAMETER_KEY = "DIAMETER_KEY"
CURRENT_SUMMER_KEY = "CURRENT_SUMMER_KEY"
CURRENT_WINTER_KEY = "CURRENT_WINTER_KEY"
COST_PER_KM_KEY = "COST_PER_KM_KEY"
GMD_KEY = "GMD_KEY"

# for towers
TOWER_TYPE_KEY = "TOWER_TYPE_KEY"
PHASE_LAYOUT_KEY = "PHASE_LAYOUT_KEY"
PHASE_SPACING_KEY = "PHASE_SPACING_KEY"
CIRCUITS_PER_PHASE_KEY = "CIRCUITS_PER_PHASE_KEY"

# for bundles
BUNDLE_TYPE_KEY = "BUNDLE_TYPE_KEY"
BUNDLE_PATTERN_KEY = "BUNDLE_PATTERN_KEY"
BUNDLE_SPACING_KEY = "BUNDLE_SPACING_KEY"
BUNDLE_WIRE_COUNT = "BUNDLE_WIRE_COUNT"

# for csv
CSV_TOWER_TYPE_KEY = "Tower Type"
CSV_TOWER_CIRCUT_NUM_KEY = "Circuits per phase"
CSV_BUNDLE_NUM_KEY = "Lines per bundle"
CSV_BUNDLE_PHASE_SPACING_KEY = "Phase spacing (m)"
CSV_BUNDLE_TYPE_KEY = "Bundle Type"
CSV_CONDUCTOR_TYPE_KEY = "Conductor Type"
CSV_RESISTANCE_KEY = "Resistance"
CSV_INDUCTANCE_KEY = "Inductance"
CSV_CAPACITANCE_KEY = "Capacitance"
CSV_IMPEDANCE_KEY = "Impedance"
CSV_ADMITTANCE_KEY = "Admittance"
CSV_A_KEY = "A"
CSV_B_KEY = "B"
CSV_C_KEY = "C"
CSV_D_KEY = "D"
CSV_VS_KEY = "Vs"
CSV_IS_KEY = "Is"
CSV_VR_MAGNITUDE_KEY = "Vr (KV)"
CSV_VR_ANGLE_KEY = "Vr angle (Degrees)"
CSV_IR_MAGNITUDE_KEY = "Ir (A)"
CSV_IR_ANGLE_KEY = "Ir angle (Degrees)"
CSV_COST_KEY = "Cost (Million $)"
CSV_POWER_LOSS_KEY = "Real Power loss (%)"
CSV_THERMAL_CURRENT_LIMIT_KEY = "Current limit per phase"
CSV_THERMAL_CURRENT_LIMIT_BOoLEAN_KEY = "Thermal limit surpassed"
CSV_SUMMER_CURRENT_MAX_KEY = "Current limit (Summer)"
CSV_WINTER_CURRENT_MAX_KEY = "Current limit (Winter)"
CSV_STABILITY_LIMIT_KEY = "Stability limit (MVA)"
CSV_STABILITY_LIMIT_ANGLE_KEY = "Stability limit angle"
CSV_DYNAMIC_STABILITY_LIMIT_KEY = "Dynamic Stability limit (MVA)"
CSV_DYNAMIC_STABILITY_LIMIT_ANGLE_KEY = "Dynamic Stability limit angle"

"""Phase layout types"""
HORIZONTAL_LAYOUT = "Horizontal phasing"
VERTICAL_LAYOUT = "Vertical phasing"
VERTICAL_LAYOUT_DOUBLE = "Vertical phasing x2"
TRIANGLE_LAYOUT = "Triangle"


# I see now that i am abusing dictionaries here and could of used a simpler data structure
class Conductors:
    nine = {
        CONDUCTOR_TYPE_KEY: "AAC 9.0 mm diameter",
        DIAMETER_KEY: 0.009,
        CURRENT_SUMMER_KEY: 110,
        CURRENT_WINTER_KEY: 308,
        COST_PER_KM_KEY: 4300
    }

    sixteen = {
        CONDUCTOR_TYPE_KEY: "AAC 16.3 mm diameter",
        DIAMETER_KEY: 0.0163,
        CURRENT_SUMMER_KEY: 216,
        CURRENT_WINTER_KEY: 636,
        COST_PER_KM_KEY: 6700
    }

    twenty_one = {
        CONDUCTOR_TYPE_KEY: "AAC 21.0 mm diameter",
        DIAMETER_KEY: 0.021,
        CURRENT_SUMMER_KEY: 299,
        CURRENT_WINTER_KEY: 875,
        COST_PER_KM_KEY: 9000
    }

    twenty_six = {
        CONDUCTOR_TYPE_KEY: "AAC 26.3 mm diameter",
        DIAMETER_KEY: 0.0263,
        CURRENT_SUMMER_KEY: 405,
        CURRENT_WINTER_KEY: 997,
        COST_PER_KM_KEY: 12300
    }

    thirty_one = {
        CONDUCTOR_TYPE_KEY: "AAC 31.5 mm diameter",
        DIAMETER_KEY: 0.0315,
        CURRENT_SUMMER_KEY: 495,
        CURRENT_WINTER_KEY: 1224,
        COST_PER_KM_KEY: 16300
    }


class Towers:
    # assume horizontal layouts are transposed
    A1 = {
        TOWER_TYPE_KEY: "Tower Type A1",
        PHASE_LAYOUT_KEY: HORIZONTAL_LAYOUT,
        PHASE_SPACING_KEY: 2.2,
        COST_PER_KM_KEY: 62000,
        CIRCUITS_PER_PHASE_KEY: 1,
        GMD_KEY: math.pow(2, 1 / 3) * 2.2
    }

    A2 = {
        TOWER_TYPE_KEY: "Tower Type A2",
        PHASE_LAYOUT_KEY: HORIZONTAL_LAYOUT,
        PHASE_SPACING_KEY: 2.7,
        COST_PER_KM_KEY: 76000,
        CIRCUITS_PER_PHASE_KEY: 1,
        GMD_KEY: math.pow(2, 1 / 3) * 2.7
    }

    B1 = {
        TOWER_TYPE_KEY: "Tower Type B1",
        PHASE_LAYOUT_KEY: VERTICAL_LAYOUT,
        PHASE_SPACING_KEY: 2.4,
        COST_PER_KM_KEY: 75000,
        CIRCUITS_PER_PHASE_KEY: 1,
        GMD_KEY: math.pow(2, 1 / 3) * 2.4
    }

    B2 = {
        TOWER_TYPE_KEY: "Tower Type B2",
        PHASE_LAYOUT_KEY: VERTICAL_LAYOUT,
        PHASE_SPACING_KEY: 3.2,
        COST_PER_KM_KEY: 86000,
        CIRCUITS_PER_PHASE_KEY: 1,
        GMD_KEY: math.pow(2, 1 / 3) * 3.2
    }

    B1_double = {
        TOWER_TYPE_KEY: "Tower Type B1 – Double",
        PHASE_LAYOUT_KEY: VERTICAL_LAYOUT,
        PHASE_SPACING_KEY: 2.4,
        COST_PER_KM_KEY: 75000,
        CIRCUITS_PER_PHASE_KEY: 2,
        GMD_KEY: math.pow(2, 1 / 3) * 2.4
    }

    B2_double = {
        TOWER_TYPE_KEY: "Tower Type B2 – Double",
        PHASE_LAYOUT_KEY: VERTICAL_LAYOUT,
        PHASE_SPACING_KEY: 2.4,
        COST_PER_KM_KEY: 86000,
        CIRCUITS_PER_PHASE_KEY: 2,
        GMD_KEY: math.pow(2, 1 / 3) * 3.2
    }

    C = {
        TOWER_TYPE_KEY: "Tower Type C",
        PHASE_LAYOUT_KEY: TRIANGLE_LAYOUT,
        PHASE_SPACING_KEY: 3.2,
        COST_PER_KM_KEY: 76000,
        CIRCUITS_PER_PHASE_KEY: 1,
        GMD_KEY: 3.2
    }


class Bundle:
    NoBundle = {
        BUNDLE_TYPE_KEY: "No bundling – 1 conductor",
        BUNDLE_PATTERN_KEY: "NA",
        BUNDLE_WIRE_COUNT: 1,
        BUNDLE_SPACING_KEY: 0,
        COST_PER_KM_KEY: 30000
    }

    Two_Conductor_24_cm = {
        BUNDLE_TYPE_KEY: "Bundling spacer – 2 conductor, 24 cm",
        BUNDLE_PATTERN_KEY: " Horizontal, 24 cm spacing",
        BUNDLE_WIRE_COUNT: 2,
        BUNDLE_SPACING_KEY: 0.24,
        COST_PER_KM_KEY: 35000
    }

    Two_Conductor_32_cm = {
        BUNDLE_TYPE_KEY: "Bundling spacer – 2 conductor, 32 cm",
        BUNDLE_PATTERN_KEY: "Horizontal, 32 cm spacing",
        BUNDLE_WIRE_COUNT: 2,
        BUNDLE_SPACING_KEY: 0.32,
        COST_PER_KM_KEY: 36000
    }

    Three_Conductor_23_cm = {
        BUNDLE_TYPE_KEY: "Bundling spacer – 3 conductor, 23 cm ",
        BUNDLE_PATTERN_KEY: " Triangle, 23 cm sides",
        BUNDLE_WIRE_COUNT: 3,
        BUNDLE_SPACING_KEY: 0.23,
        COST_PER_KM_KEY: 40000
    }

    Three_Conductor_33_cm = {
        BUNDLE_TYPE_KEY: "Bundling spacer – 3 conductor, 33 cm",
        BUNDLE_PATTERN_KEY: "Triangle, 33 cm sides",
        BUNDLE_WIRE_COUNT: 3,
        BUNDLE_SPACING_KEY: 0.33,
        COST_PER_KM_KEY: 42000
    }

    Four_Conductor_26_cm = {
        BUNDLE_TYPE_KEY: "Bundling spacer – 4 conductor, 26 cm",
        BUNDLE_PATTERN_KEY: "Square, 25 cm sides ",
        BUNDLE_WIRE_COUNT: 4,
        BUNDLE_SPACING_KEY: 0.25,
        COST_PER_KM_KEY: 45000
    }


"""Line Constants"""
rho_aluminium = 2.83e-8  # the rho for aluminium per meter, at 20 degreesC
temp_coefficient_aluminium = 228
frequency = 50
line_packing_factor = 0.9
line_skin_effect = 1.1


def resistance(rho_conductor, temp_coefficient, diameter, packing_factor, skin_effect):
    Area = math.pi * math.pow(diameter / 2, 2) * packing_factor
    R = rho_conductor * (1000 / Area) * skin_effect  # ohms @ 20 degrees C
    return R * (temp_coefficient + 50) / (temp_coefficient + 20)  # ohms @ 50 degrees C


def inductance(GMD, GMR):
    l = 0.2 * np.log(GMD / GMR)  # mH/km
    return l / 1000


def capacitance(GMD, GMR):
    c = 0.0556 / np.log(GMD / GMR)  # uF/km
    return c / 1000000


def power_stability_limit(Vs, Vr, A, B, delta):
    # delta in radians
    return (abs(Vs)*abs(Vr) / abs(B)) * math.cos(cmath.polar(B)[1] - delta) - (
                abs(A) * math.pow(abs(Vr), 2) / abs(B)) * math.cos(cmath.polar(B)[1]-cmath.polar(A)[1])


def gen_csv(length, conductor_list, bundle_list, tower_list):
    configurations = []  # list of configurations (list of configuration)

    for tower in tower_list:

        for conductor in conductor_list:

            for bundle in bundle_list:

                if tower == Towers.B2_double or tower == Towers.B1_double:
                    conductor_count_per_phase = 2 * bundle[BUNDLE_WIRE_COUNT]
                else:
                    conductor_count_per_phase = bundle[BUNDLE_WIRE_COUNT]

                # getting the GMR of the line considering bundle and conductor
                radius_prime = math.pow(math.e, -1 / 4) * conductor[DIAMETER_KEY] / 2
                if bundle[BUNDLE_WIRE_COUNT] == 1:
                    GMR = radius_prime
                elif bundle[BUNDLE_WIRE_COUNT] == 2:
                    GMR = math.pow(radius_prime * bundle[BUNDLE_SPACING_KEY], 1 / 2)
                elif bundle[BUNDLE_WIRE_COUNT] == 3:
                    GMR = math.pow((radius_prime * math.pow(bundle[BUNDLE_SPACING_KEY], 2)), 1 / 3)
                else:
                    GMR = math.pow((radius_prime * math.sqrt(2) * math.pow(bundle[BUNDLE_SPACING_KEY], 3)), 1 / 4)

                r = resistance(rho_conductor=rho_aluminium, temp_coefficient=temp_coefficient_aluminium,
                               diameter=conductor[DIAMETER_KEY], packing_factor=line_packing_factor,
                               skin_effect=line_skin_effect) / conductor_count_per_phase
                l = inductance(GMD=tower[GMD_KEY], GMR=GMR)
                c = capacitance(GMD=tower[GMD_KEY], GMR=GMR)

                z = r + 2j * math.pi * l * frequency
                y = 2j * math.pi * c * frequency

                gamma = cmath.sqrt(z * y)

                Zc = cmath.sqrt(z / y)
                A = cmath.cosh(gamma * length)
                B = Zc * cmath.sinh(gamma * length)
                C = (1 / Zc) * cmath.sinh(gamma * length)
                D = cmath.cosh(gamma * length)

                """Line voltages and power"""
                Vs = 132 * math.pow(10, 3)
                S_3_phase_sent = 160 * math.pow(10, 6)
                Is = S_3_phase_sent / (math.sqrt(3) * Vs)

                Vr = (1 / (C - (A * D / B))) * (Is - (D / B) * Vs)

                Ir = (Vs - A * Vr) / B

                Cost = (3 * bundle[COST_PER_KM_KEY] + tower[COST_PER_KM_KEY] + 3 * conductor[
                    COST_PER_KM_KEY] * conductor_count_per_phase) * length
                Losses = (160 * math.pow(10, 6) - (math.sqrt(3) * Vr * Ir.conjugate()).real) / (
                        160 * math.pow(10, 6)) * 100

                stability_limit_angle = cmath.polar(B)[1]
                stability_limit = power_stability_limit(Vs=Vs, Vr=Vr, A=A, B=B, delta=stability_limit_angle)
                stability_limit_angle = cmath.polar(B)[1] * 180 / math.pi  # Convert to degrees for csv

                dynamic_stability_limit_angle = cmath.polar(B)[1]/2
                dynamic_stability_limit = power_stability_limit(Vs=Vs, Vr=Vr, A=A, B=B, delta=dynamic_stability_limit_angle)
                dynamic_stability_limit_angle = dynamic_stability_limit_angle * 180 / math.pi  # Convert to degrees for CSV

                current_per_conductor = round(Is.real/(tower[CIRCUITS_PER_PHASE_KEY]*bundle[BUNDLE_WIRE_COUNT]))
                if (current_per_conductor>conductor[CURRENT_SUMMER_KEY]*.75):
                    surpassed = True
                else:
                    surpassed = False

                # Convert to polar for excel
                Vr = cmath.polar(Vr)
                Ir = cmath.polar(Ir)

                configuration = {
                    CSV_TOWER_TYPE_KEY: tower[TOWER_TYPE_KEY],
                    CSV_BUNDLE_TYPE_KEY: bundle[BUNDLE_TYPE_KEY],
                    CSV_CONDUCTOR_TYPE_KEY: conductor[CONDUCTOR_TYPE_KEY],
                    CSV_IMPEDANCE_KEY: complex(round(z.real, 3), round(z.imag, 3)),
                    CSV_ADMITTANCE_KEY: complex(y.real, y.imag),
                    CSV_A_KEY: complex(round(A.real, 3), round(A.imag, 3)),
                    CSV_B_KEY: complex(round(B.real, 3), round(B.imag, 3)),
                    CSV_C_KEY: complex(round(C.real, 3), round(C.imag, 3)),
                    CSV_D_KEY: complex(round(D.real, 3), round(D.imag, 3)),
                    CSV_VS_KEY: round(Vs/1000, 1),
                    CSV_IS_KEY: round(Is.real, 1),
                    CSV_VR_MAGNITUDE_KEY: round(Vr[0]/1000, 1),
                    CSV_VR_ANGLE_KEY: round(Vr[1] * 180 / math.pi, 1),
                    CSV_IR_MAGNITUDE_KEY: round(Ir[0], 1),
                    CSV_IR_ANGLE_KEY: round(Ir[1] * 180 / math.pi, 1),
                    CSV_COST_KEY: round(Cost/1000000, 1),
                    CSV_POWER_LOSS_KEY: round(Losses, 2),
                    CSV_THERMAL_CURRENT_LIMIT_BOoLEAN_KEY: surpassed,
                    CSV_SUMMER_CURRENT_MAX_KEY: conductor[CURRENT_SUMMER_KEY],
                    CSV_WINTER_CURRENT_MAX_KEY: conductor[CURRENT_WINTER_KEY],
                    CSV_STABILITY_LIMIT_KEY: round(stability_limit/1000000, 2),
                    CSV_STABILITY_LIMIT_ANGLE_KEY: round(stability_limit_angle, 1),
                    CSV_DYNAMIC_STABILITY_LIMIT_KEY: round(dynamic_stability_limit/1000000, 2),
                    CSV_DYNAMIC_STABILITY_LIMIT_ANGLE_KEY: round(dynamic_stability_limit_angle, 1)
                }
                configurations.append(configuration)

    with open(str(length) + "km.csv", "w", newline="") as file:
        fieldnames = [CSV_TOWER_TYPE_KEY, CSV_BUNDLE_TYPE_KEY, CSV_CONDUCTOR_TYPE_KEY, CSV_IMPEDANCE_KEY,
                      CSV_ADMITTANCE_KEY, CSV_A_KEY, CSV_B_KEY,
                      CSV_C_KEY, CSV_D_KEY, CSV_VS_KEY, CSV_IS_KEY, CSV_VR_MAGNITUDE_KEY, CSV_VR_ANGLE_KEY,
                      CSV_IR_MAGNITUDE_KEY, CSV_IR_ANGLE_KEY, CSV_COST_KEY, CSV_POWER_LOSS_KEY, CSV_THERMAL_CURRENT_LIMIT_BOoLEAN_KEY,
                      CSV_SUMMER_CURRENT_MAX_KEY, CSV_WINTER_CURRENT_MAX_KEY, CSV_STABILITY_LIMIT_KEY,
                      CSV_STABILITY_LIMIT_ANGLE_KEY, CSV_DYNAMIC_STABILITY_LIMIT_KEY,
                      CSV_DYNAMIC_STABILITY_LIMIT_ANGLE_KEY]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for configuration in configurations:
            writer.writerow(configuration)


conductor_list = [Conductors.nine, Conductors.sixteen, Conductors.twenty_one, Conductors.twenty_six,
                  Conductors.thirty_one]
bundle_list = [Bundle.NoBundle, Bundle.Two_Conductor_24_cm, Bundle.Two_Conductor_32_cm, Bundle.Three_Conductor_23_cm,
               Bundle.Three_Conductor_33_cm, Bundle.Four_Conductor_26_cm]
tower_list = [Towers.A1, Towers.A2, Towers.B1, Towers.B2, Towers.B1_double, Towers.B2_double, Towers.C]

gen_csv(length=227, conductor_list=conductor_list, bundle_list=bundle_list, tower_list=tower_list)
#
# # Proof of concept for tower C1, conductor nine, 33 bundle 33cm
# length = 224
#
# # line resistance
# R = resistance(rho_aluminium, temp_coefficient_aluminium, Conductors.nine[DIAMETER_KEY], line_packing_factor, line_skin_effect)/3
#
# radius_prime = math.pow(math.e, -1 / 4) * Conductors.nine[DIAMETER_KEY] / 2
# print(radius_prime)
# GMR = math.pow(radius_prime*math.pow(Bundle.Three_Conductor_33_cm[BUNDLE_SPACING_KEY], 2), 1/3)
# print(math.pow(Bundle.Three_Conductor_33_cm[BUNDLE_SPACING_KEY], 2))
# print(GMR)
# L = inductance(Towers.B1[GMD_KEY], GMR)
#
# print("R")
# print(R)
# print("L")
# print(L)
#
# C = capacitance(Towers.B1[GMD_KEY], GMR)
# print("C")
# print(C)
#
# Z = R + 2j * math.pi * L * frequency
# Y = 2j * math.pi * C * frequency
#
# print("Z")
# print(complex(round(Z.real, 3), round(Z.imag, 3)),)
# print("Y")
# print(Y)
#
# gamma = cmath.sqrt(Z * Y)
# print("gamma")
# print(complex(round(gamma.real, 3), round(gamma.imag, 3)),)
#
# """Long line model"""
# Zc = cmath.sqrt(Z / Y)
# A = cmath.cosh(gamma * length)
# B = Zc * cmath.sinh(gamma * length)
# C = (1 / Zc) * cmath.sinh(gamma * length)
# D = cmath.cosh(gamma * length)
#
# print("Zc")
# print(complex(round(Zc.real, 3), round(Zc.imag, 3)))
# print("A")
# print(complex(round(A.real, 3), round(A.imag, 3)))
# print("B")
# print(complex(round(B.real, 3), round(B.imag, 3)))
# print("C")
# print(complex(round(C.real, 3), round(C.imag, 3)))
# print("D")
# print(complex(round(D.real, 3), round(D.imag, 3)))
#
# """Line voltages and power"""
# Vs = 132 * math.pow(10, 3)
# S_3_phase_sent = 160 * math.pow(10, 6)
# Is = S_3_phase_sent / (math.sqrt(3) * Vs)
# print("Is")
# print(complex(round(Is.real, 3), round(Is.imag, 3)))
#
# Vr = (1 / (C - (A * D / B))) * (Is - (D / B) * Vs)
# print("Vr")
# print(complex(round(Vr.real, 3), round(Vr.imag, 3)))
#
# Ir = (Vs - A * Vr) / B
# print("Ir")
# print(complex(round(Ir.real, 3), round(Ir.imag, 3)))
#
