# This code is for HW5 Grading purpose
# created by Mukhamad Suhermanto
'''
This is for grading a calculation of Technology Matrix, Intervention Matrix.
The inputs used in this is Technology Matrix, Intervention Matrix, and Final Demand Matrix.
'''
import pandas as pd
import numpy as np

# Naming the matrix
techMat = 'data/tech_matrix.csv'# Technology Matrix
intervMat = 'data/intervMat.csv'#Intervention Matrix
fdemand1 = 'data/fdemand1.csv'#Final Demand with 1 MJ of corn ethanol

def csvToMatrix(fileName):
    fileName = pd.read_csv(fileName)
    fileName = pd.DataFrame(fileName).fillna(0)
    fileName = fileName.apply(pd.to_numeric, errors='coerce').dropna(axis='columns').to_numpy(dtype=float,na_value=0)
    return fileName

#Converting the csv files into matrix, ready for calculation process
techMat=csvToMatrix(techMat)
intervMat=csvToMatrix(intervMat)
fdemand1 = pd.read_csv(fdemand1).values #turn fdemand table in csv format to an array

# Function to calculate emission
def calc_emission(technology_matrix, final_demand, intervention_matrix):
    '''
    calc_emission
    is used to calculate the emission from matrix.
    It takes three arguments, namely:
                        1) technology_matrix;
                        2) final_demand;
                        3) intervention_matrix
    '''
    technology_matrix_inv = np.linalg.inv(technology_matrix)
    scale_matrix = np.dot(technology_matrix_inv, final_demand)
    result_matrix = np.dot(intervention_matrix, scale_matrix)
    np.savetxt("data/result.csv", result_matrix, delimiter=",")
    print (result_matrix)

# Calculating the emission of each contributor and total here
result = pd.read_csv('data/result.csv', names=['kg'])# Technology Matrix
emission = result['kg']
CO2=emission[0] # 1st Row is CO2
CH4=emission[1] # 2nd Row is CH4
N2O=emission[2] # 3rd Row is N2O
CO2eq_CH4 = CH4 * 28  # CO2-eq from CH4, CH4*28
CO2eq_N2O = N2O * 265 # CO2-eq from N2O, CH4*265
CO2_tot_kggal = CO2 + CO2eq_CH4 +CO2eq_N2O
MJ_per_gal = 89 # 1 gallon equals 89 MJ of ethanol, 
                    # https://www.ocean.washington.edu/courses/envir215/energynumbers.pdf
kg_to_g = 1000 # converting kg to g, the original emission is in kg
CO2_tot_gPerMJ = CO2_tot_kggal * kg_to_g / MJ_per_gal

# Making tabulated result ---> save to csv
CO2_CO2e_gPerMJ = CO2 * kg_to_g / MJ_per_gal
CH4_CO2e_gPerMJ = CO2eq_CH4 * kg_to_g / MJ_per_gal
N2O_CO2e_gPerMJ = CO2eq_N2O * kg_to_g / MJ_per_gal

# Total/Accumulative
kg_total = CO2 + CH4 + N2O
CO2eq_kgPerGal_total = CO2 + CO2eq_CH4 + CO2eq_N2O
CO2e_gPerMJ_total = CO2_CO2e_gPerMJ + CH4_CO2e_gPerMJ + N2O_CO2e_gPerMJ

headerList = [ "kg", "kg CO2e/gal", "g CO2e/MJ"]
emissionList = ["CO2", "CH4", "N2O", "TOTAL"]
data = np.array([[CO2,CO2, CO2_CO2e_gPerMJ],
                [CH4,CO2eq_CH4, CH4_CO2e_gPerMJ],
                [N2O,CO2eq_N2O, N2O_CO2e_gPerMJ],
                [kg_total, CO2eq_kgPerGal_total, CO2e_gPerMJ_total]])

data_result = pd.DataFrame(data, emissionList, headerList )
np.savetxt("data/data_result.csv", data_result, delimiter=",")
print('The tabulated results are as following:')
print('---------------------------------------')
print(data_result)
print('---------------------------------------')
print (f'The total CO2 equivalent obtained from this calculation is {CO2_tot_kggal:.6} kg CO2e/gallon ethanol.')
print (f'With all necessary unit conversions, the CO2 equivalent amount is {CO2_tot_gPerMJ:.6} g CO2e/MJ ethanol.')

# Getting the error
#Based on Prof. Zhao's announcement, per gallon of ethanol
CO2_ref = 2.9 #kg;
CH4_ref = 0.024 #kg;
N2O_ref = 0.0011 #kg;

# Result Error comparison
CO2_error = (CO2_ref-CO2)/CO2_ref*100
CH4_error = (CH4_ref-CH4)/CH4_ref*100
N2O_error = (N2O_ref-N2O)/N2O_ref*100

headerList = [ "Reference", "Results", "Error %"]
emissionList = ["CO2", "CH4", "N2O"]
data = np.array([[CO2_ref, CO2, CO2_error],
                [CH4_ref, CH4, CH4_error],
                [N2O_ref, N2O, N2O_ref]])

error_result = pd.DataFrame(data, emissionList, headerList )
np.savetxt("data/error_result.csv", error_result, delimiter=",")
print('The Results Error are as following:')
print('---------------------------------------')
print(error_result)

# Result Error comparison version 2
# If the result is bigger than the reference
CO2_error = (CO2-CO2_ref)/CO2*100
CH4_error = (CH4-CH4_ref)/CH4*100
N2O_error = (N2O-N2O_ref)/N2O*100
headerList = [ "Reference", "Results", "Error %"]
emissionList = ["CO2", "CH4", "N2O"]
data = np.array([[CO2_ref, CO2, CO2_error2],
                [CH4_ref, CH4, CH4_error2],
                [N2O_ref, N2O, N2O_ref2]])

error_result2 = pd.DataFrame(data, emissionList, headerList )
np.savetxt("data/error_result2.csv", error_result2, delimiter=",")
print('The Results Error are as following:')
print('---------------------------------------')
print(error_result2)


