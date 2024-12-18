"""
Library Features:

Name:          lib_default_namelist
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241125'
Version:       '4.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# namelist type and default values
type_namelist_default_hmc = dict(

    HMC_Parameters={
        'dUc': 'default',
        'dUh': 'default',
        'dCt': 'default',
        'dCf': 'default',
        'dCPI': 'default',
        'dCN': 'default',
        'dWS': 'default',
        'dWDL': 'default',
        'dFrac': 'default',
        'dWTableHbr': 'default',
        'dKSatRatio': 'default',
        'dSlopeMax': 'default',
        'dSoil_ksat_infilt': 'default',
        'dSoil_ksat_drain': 'default',
        'dSoil_vmax': 'default',
        'dWtable_ksath': 'default',
        'sDomainName': 'mandatory',
    },

    HMC_Namelist={

        'iFlagDebugSet': 'default',
        'iFlagDebugLevel': 'default',

        'iFlagTypeData_Static': 'default',
        'iFlagTypeData_Forcing_Gridded': 'default',
        'iFlagTypeData_Forcing_Point': 'default',
        'iFlagTypeData_Forcing_TimeSeries': 'default',
        'iFlagTypeData_Updating_Gridded': 'default',
        'iFlagTypeData_Output_Gridded': 'default',
        'iFlagTypeData_Output_Point': 'default',
        'iFlagTypeData_Output_TimeSeries': 'default',
        'iFlagTypeData_State_Gridded': 'default',
        'iFlagTypeData_State_Point': 'default',
        'iFlagTypeData_Restart_Gridded': 'default',
        'iFlagTypeData_Restart_Point': 'default',

        'iFlagOs': 'default',
        'iFlagFlowDeep': 'default',
        'iFlagRestart': 'default',
        'iFlagVarDtPhysConv': 'default',
        'iFlagSnow': 'default',
        'iFlagSnowAssim': 'default',
        'iFlagSMAssim': 'default',
        'iFlagLAI': 'default',
        'iFlagAlbedo': 'default',
        'iFlagCoeffRes': 'default',
        'iFlagWS': 'default',
        'iFlagWDL': 'default',
        'iFlagReleaseMass': 'default',
        'iFlagCType': 'default',
        'iFlagFrac': 'default',
        'iFlagDynVeg': 'default',
        'iFlagFlood': 'default',
        'iFlagEnergyBalance': 'default',
        'iFlagSoilParamsType': 'default',
        'iFlagInfiltRateVariable': 'default',
        'iFlagBetaET': 'default',

        'a1dGeoForcing': 'default',
        'a1dResForcing': 'default',
        'a1iDimsForcing': 'default',

        'iSimLength': 'mandatory',
        'iDtModel': 'mandatory',

        'iDtPhysMethod': 'default',
        'iDtPhysConv': 'default',
        'a1dDemStep': 'default',
        'a1dIntStep': 'default',
        'a1dDtStep': 'default',
        'a1dDtRatioStep': 'default',

        'iDtData_Forcing': 'mandatory',
        'iDtData_Updating': 'mandatory',
        'iDtData_Output_Gridded': 'mandatory',
        'iDtData_Output_Point': 'mandatory',
        'iDtData_State_Gridded': 'mandatory',
        'iDtData_State_Point': 'mandatory',

        'iActiveData_Output_Generic': 'default',
        'iActiveData_Output_Flooding': 'default',
        'iActiveData_Output_Snow': 'default',
        'iAccumData_Output_Hour': 'default',

        'iScaleFactor': 'default',
        'iTcMax': 'default',
        'iTVeg': 'default',

        'sTimeStart':  'mandatory',
        'sTimeRestart':  'mandatory',

        'sPathData_Static_Gridded': 'mandatory',
        'sPathData_Static_Point':  'mandatory',
        'sPathData_Forcing_Gridded':  'mandatory',
        'sPathData_Forcing_Point':  'mandatory',
        'sPathData_Forcing_TimeSeries':  'mandatory',
        'sPathData_Updating_Gridded':  'mandatory',
        'sPathData_Output_Gridded':  'mandatory',
        'sPathData_Output_Point':  'mandatory',
        'sPathData_Output_TimeSeries':  'mandatory',
        'sPathData_State_Gridded':   'mandatory',
        'sPathData_State_Point':  'mandatory',
        'sPathData_Restart_Gridded':  'mandatory',
        'sPathData_Restart_Point':  'mandatory',

    },

    HMC_Snow={
        'a1dArctUp': 'default',
        'a1dExpRhoLow': 'default',
        'a1dExpRhoHigh': 'default',
        'a1dAltRange': 'default',
        'iGlacierValue': 'default',
        'dRhoSnowFresh': 'default',
        'dRhoSnowMax': 'default',
        'dSnowQualityThr': 'default',
        'dMeltingTRef': 'default',
    },

    HMC_Constants={
        'a1dAlbedoMonthly': 'default',
        'a1dLAIMonthly': 'default',

        'dWTableHMin': 'default',
        'dWTableHUSoil': 'default',
        'dWTableHUChannel': 'default',
        'dWTableSlopeBM': 'default',
        'dWTableHOBedRock': 'default',

        'dRateMin': 'default',
        'dRateRescaling': 'default',
        'dBc': 'default',
        'dWTLossMax': 'default',
        'dPowVarInfiltRate': 'default',

        'dTRef': 'default',
        'iTdeepShift': 'default',
        'a1dCHMonthly': 'default',
        'dEpsS': 'default',
        'dSigma': 'default',
        'dBFMin': 'default',
        'dBFMax': 'default',
        'dLSTDeltaMax': 'default',

        'dZRef': 'default',
        'dG': 'default',
        'dCp': 'default',
        'dRd': 'default',

        'dRhoS': 'default',
        'dRhoW': 'default',
        'dCpS': 'default',
        'dCpW': 'default',
        'dKq': 'default',
        'dKw': 'default',
        'dKo': 'default',
        'dPorS': 'default',
        'dFqS': 'default',

        'dTV': 'default',
        'dDamSpillH': 'default',

        'dSMGain': 'default'
    },

    HMC_Command={
        'sCommandZipFile': 'default',
        'sCommandUnzipFile': 'default',
        'sCommandRemoveFile': 'default',
        'sCommandCreateFolder': 'default',
    },

    HMC_Info={
        'sReleaseVersion': 'default',
        'sAuthorNames': 'default',
        'sReleaseDate': 'default',
    },
)
# Namelist constants
structure_namelist_default_hmc = dict(

    HMC_Parameters={
        'dUc': 20,
        'dUh': 1.5,
        'dCt': 0.5,
        'dCf': 0.02,
        'dCPI': 0.3,
        'dCN': 60.01,
        'dWS': 3.6780000000000003e-09,
        'dWDL': 3.6780000000000003e-09,
        'dFrac': 0.0,
        'dWTableHbr': 500,
        'dKSatRatio': 1,
        'dSlopeMax': 70,
        'dSoil_ksat_infilt': 3.5,
        'dSoil_ksat_drain': 3.5,
        'dSoil_vmax': 500,
        'dWtable_ksath': 1,
        'sDomainName': None
    },

    HMC_Namelist={

        'iFlagDebugSet': 1,
        'iFlagDebugLevel': 3,

        'iFlagTypeData_Static': 1,
        'iFlagTypeData_Forcing_Gridded': 2,
        'iFlagTypeData_Forcing_Point': 1,
        'iFlagTypeData_Forcing_TimeSeries': 1,
        'iFlagTypeData_Updating_Gridded': 2,
        'iFlagTypeData_Output_Gridded': 2,
        'iFlagTypeData_Output_Point': 1,
        'iFlagTypeData_Output_TimeSeries': 1,
        'iFlagTypeData_State_Gridded': 2,
        'iFlagTypeData_State_Point': 1,
        'iFlagTypeData_Restart_Gridded': 2,
        'iFlagTypeData_Restart_Point': 1,

        'iFlagOs': 10,
        'iFlagFlowDeep': 1,
        'iFlagRestart': 1,
        'iFlagVarDtPhysConv': 1,
        'iFlagSnow': 0,
        'iFlagSnowAssim': 0,
        'iFlagSMAssim': 0,
        'iFlagLAI': 0,
        'iFlagAlbedo': 0,
        'iFlagCoeffRes': 1,
        'iFlagWS': 0,
        'iFlagWDL': 0,
        'iFlagReleaseMass': 1,
        'iFlagCType': 1,
        'iFlagFrac': 0,
        'iFlagDynVeg': 1,
        'iFlagFlood': 0,
        'iFlagEnergyBalance': 1,
        'iFlagSoilParamsType': 1,
        'iFlagInfiltRateVariable': 2,
        'iFlagBetaET': 1,

        'a1dGeoForcing': [-9999.0, -9999.0],
        'a1dResForcing': [-9999.0, -9999.0],
        'a1iDimsForcing': [-9999, -9999],

        'iSimLength': None,
        'iDtModel': None,

        'iDtPhysMethod': 1,
        'iDtPhysConv': 50,
        'a1dDemStep': [1, 10, 100, 1000],
        'a1dIntStep': [1, 5, 25, 600],
        'a1dDtStep': [1, 6, 6, 60],
        'a1dDtRatioStep': [3, 3, 3, 2],

        'iDtData_Forcing': None,
        'iDtData_Updating': None,
        'iDtData_Output_Gridded': None,
        'iDtData_Output_Point': None,
        'iDtData_State_Gridded': None,
        'iDtData_State_Point': None,

        'iActiveData_Output_Generic': 2,
        'iActiveData_Output_Flooding': 0,
        'iActiveData_Output_Snow': 0,
        'iAccumData_Output_Hour': 23,

        'iScaleFactor': 10,
        'iTcMax': -9999,
        'iTVeg': 720,

        'sTimeStart': None,
        'sTimeRestart': None,

        'sPathData_Static_Gridded': None,
        'sPathData_Static_Point': None,
        'sPathData_Forcing_Gridded': None,
        'sPathData_Forcing_Point': None,
        'sPathData_Forcing_TimeSeries': None,
        'sPathData_Updating_Gridded': None,
        'sPathData_Output_Gridded': None,
        'sPathData_Output_Point': None,
        'sPathData_Output_TimeSeries': None,
        'sPathData_State_Gridded': None,
        'sPathData_State_Point': None,
        'sPathData_Restart_Gridded': None,
        'sPathData_Restart_Point': None,

    },

    HMC_Snow={
        'a1dArctUp': [3.0, 4.5, 3.0, 4.0],
        'a1dExpRhoLow': [0.0333, 0.0222, 0.0250, 0.0333],
        'a1dExpRhoHigh': [0.0714, 0.0714, 0.0714, 0.0714],
        'a1dAltRange': [1500.0, 2000.0, 2500.0, 2500.0],
        'iGlacierValue': 2,
        'dRhoSnowFresh': 100,
        'dRhoSnowMax': 400,
        'dSnowQualityThr': 0.3,
        'dMeltingTRef': 1,
    },

    HMC_Constants={
        'a1dAlbedoMonthly': [0.18,  0.17, 0.16,  0.15,  0.15,  0.15,  0.15,  0.16,  0.16,  0.17,  0.17,  0.18],
        'a1dLAIMonthly': [4.00,  4.00, 4.00,  4.00,  4.00,  4.00,  4.00,  4.00,  4.00,  4.00,  4.00,  4.00],

        'dWTableHMin': 10.0,
        'dWTableHUSoil': 100.0,
        'dWTableHUChannel': 5.0,
        'dWTableSlopeBM': 0.08,
        'dWTableHOBedRock': 25.0,

        'dRateMin': 0.01,
        'dRateRescaling': 1.0,
        'dBc': 0.5,
        'dWTLossMax': 0.25,
        'dPowVarInfiltRate': 7,

        'dTRef': 273.15,
        'iTdeepShift': 2,
        'a1dCHMonthly': [-7.3, -7.3, -5.8, -5.8, -5.8, -4.8, -4.8, -4.8, -4.8, -5.9, -5.9, -7.3],
        'dEpsS': 0.96,
        'dSigma': 0.00000005576,
        'dBFMin': 0.1,
        'dBFMax': 0.9,
        'dLSTDeltaMax': 40,

        'dZRef': 3.0,
        'dG': 9.81,
        'dCp': 1004.0,
        'dRd': 287.0,

        'dRhoS': 2700,
        'dRhoW': 1000,
        'dCpS': 733,
        'dCpW': 4186,
        'dKq': 7.7,
        'dKw': 0.57,
        'dKo': 4,
        'dPorS': 0.4,
        'dFqS': 0.5,

        'dTV': 0.95,
        'dDamSpillH': 0.4,

        'dSMGain': 0.45,
    },

    HMC_Command={
        'sCommandZipFile': "gzip -f filenameunzip > LogZip.txt",
        'sCommandUnzipFile': "gunzip -c filenamezip > filenameunzip",
        'sCommandRemoveFile': "rm filename",
        'sCommandCreateFolder': "mkdir -p path",
    },

    HMC_Info={
        'sReleaseVersion': "3.2.0",
        'sAuthorNames': "Delogu F., Silvestro F., Gabellani S., Libertino A., Ercolani G.",
        'sReleaseDate': "2022/11/25",
    },
)
# ----------------------------------------------------------------------------------------------------------------------
