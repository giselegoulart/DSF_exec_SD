# -*- coding: utf-8 -*-
from __future__ import division, print_function
import numpy as np
import os, sys
import pandas as pd
import time
#from scipy import stats
import pygmo as pg
import subprocess
import random
#from html.parser import HTMLParser

try:
    from html.parser import HTMLParseError
except ImportError:  # Python 3.5+
    class HTMLParseError(Exception):
        pass
#===============================================================================

def gen_idf(x):

    idf_file='''!-Generator IDFEditor 1.47
!-Option SortedOrder
!-NOTE: All comments with '!-' are ignored by the IDFEditor and are generated automatically.
!-      Use '!' comments if they need to be retained when using the IDFEditor.
!-   ===========  ALL OBJECTS IN CLASS: VERSION ===========

  Version,9.0;

!-   ===========  ALL OBJECTS IN CLASS: SIMULATIONCONTROL ===========

  SimulationControl,
    No,                      !- Do Zone Sizing Calculation
    No,                      !- Do System Sizing Calculation
    No,                      !- Do Plant Sizing Calculation
    Yes,                     !- Run Simulation for Sizing Periods
    Yes;                     !- Run Simulation for Weather File Run Periods

!-   ===========  ALL OBJECTS IN CLASS: BUILDING ===========

  Building,
    Pesq_fachada,            !- Name
    '''+str(x[2])+''',                     !- North Axis {deg}
    Suburbs,                 !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullExterior,            !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    ;                        !- Minimum Number of Warmup Days

!-   ===========  ALL OBJECTS IN CLASS: TIMESTEP ===========

  Timestep,6;

!-   ===========  ALL OBJECTS IN CLASS: SITE:LOCATION ===========

  Site:Location,
    VICOSA,                  !- Name
    -20.45,                  !- Latitude {deg}
    -42.52,                  !- Longitude {deg}
    -3.0,                    !- Time Zone {hr}
    650;                     !- Elevation {m}

!-   ===========  ALL OBJECTS IN CLASS: RUNPERIOD ===========

  RunPeriod,
    Ano Completo,            !- Name
    1,                       !- Begin Month
    1,                       !- Begin Day of Month
    ,                        !- Begin Year
    12,                      !- End Month
    31,                      !- End Day of Month
    ,                        !- End Year
    ,                        !- Day of Week for Start Day
    No,                      !- Use Weather File Holidays and Special Days
    No,                      !- Use Weather File Daylight Saving Period
    No,                      !- Apply Weekend Holiday Rule
    No,                      !- Use Weather File Rain Indicators
    No,                      !- Use Weather File Snow Indicators
    ;                        !- Treat Weather as Actual

!-   ===========  ALL OBJECTS IN CLASS: RUNPERIODCONTROL:DAYLIGHTSAVINGTIME ===========
! Daylight Saving Period in US

  RunPeriodControl:DaylightSavingTime,
    2nd Sunday in March,     !- Start Date
    1st Sunday in November;  !- End Date

!-   ===========  ALL OBJECTS IN CLASS: SITE:GROUNDTEMPERATURE:BUILDINGSURFACE ===========

  Site:GroundTemperature:BuildingSurface,21.81,21.89,21.87,21.76,21.51,21.36,21.26,21.43,21.51,21.62,21.76,21.78;

!-   ===========  ALL OBJECTS IN CLASS: SCHEDULETYPELIMITS ===========

  ScheduleTypeLimits,
    Any Number;              !- Name

  ScheduleTypeLimits,
    Fraction,                !- Name
    0.0,                     !- Lower Limit Value
    1.0,                     !- Upper Limit Value
    CONTINUOUS;              !- Numeric Type

  ScheduleTypeLimits,
    Temperature,             !- Name
    -60,                     !- Lower Limit Value
    200,                     !- Upper Limit Value
    CONTINUOUS;              !- Numeric Type

  ScheduleTypeLimits,
    On/Off,                  !- Name
    0,                       !- Lower Limit Value
    1,                       !- Upper Limit Value
    DISCRETE;                !- Numeric Type

  ScheduleTypeLimits,
    Control Type,            !- Name
    0,                       !- Lower Limit Value
    4,                       !- Upper Limit Value
    DISCRETE;                !- Numeric Type

  ScheduleTypeLimits,
    Humidity,                !- Name
    10,                      !- Lower Limit Value
    90,                      !- Upper Limit Value
    CONTINUOUS;              !- Numeric Type

  ScheduleTypeLimits,
    Taxas_metabolicas,       !- Name
    50,                      !- Lower Limit Value
    500,                     !- Upper Limit Value
    Continuous,              !- Numeric Type
    Dimensionless;           !- Unit Type

!-   ===========  ALL OBJECTS IN CLASS: SCHEDULE:COMPACT ===========

  Schedule:Compact,
    Always On,               !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,1.0;        !- Field 3

  Schedule:Compact,
    Always Off,              !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,0.0;        !- Field 3

  Schedule:Compact,
    Ocupacao,                !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 07:00,0,          !- Field 3
    Until: 8:00,.5,          !- Field 5
    Until: 12:00,1,          !- Field 7
    Until: 14:00,.5,         !- Field 9
    Until: 18:00,1,          !- Field 11
    Until: 19:00,.5,         !- Field 13
    Until: 24:00,0,          !- Field 15
    For: Allotherdays,       !- Field 17
    Until: 24:00,0;          !- Field 18

  Schedule:Compact,
    metabolismo_esc,         !- Name
    Taxas_metabolicas,       !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,130;        !- Field 3

  Schedule:Compact,
    Ocupacao_Ex,             !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 08:00,0,          !- Field 3
    Until: 09:00,.3,         !- Field 5
    Until: 12:00,1,          !- Field 7
    Until: 24:00,0,          !- Field 9
    For: Allotherdays,       !- Field 11
    Until: 24:00,0;          !- Field 12

  Schedule:Compact,
    Ilum_Total,              !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: Weekdays,           !- Field 2
    Until: 08:00,0,          !- Field 3
    Until: 18:00,1,          !- Field 5
    Until: 24:00,0,          !- Field 7
    For: Allotherdays,       !- Field 9
    Until: 24:00,0;          !- Field 10

  Schedule:Compact,
    Equip_esc,               !- Name
    Fraction,                !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: Weekdays,           !- Field 2
    Until: 08:00,0,          !- Field 3
    Until: 09:00,.5,         !- Field 5
    Until: 18:00,1,          !- Field 7
    Until: 24:00,0,          !- Field 9
    For: Allotherdays,       !- Field 11
    Until: 24:00,0;          !- Field 12

  Schedule:Compact,
    AberturaJanelas,         !- Name
    Temperature,             !- Schedule Type Limits Name
    Through: 12/31,          !- Field 1
    For: AllDays,            !- Field 2
    Until: 24:00,20;         !- Field 3

!-   ===========  ALL OBJECTS IN CLASS: MATERIAL ===========

  Material,
    Alvenaria_1_5_Argamassa, !- Name
    Smooth,                  !- Roughness
    0.025,                   !- Thickness {m}
    1.15,                    !- Conductivity {W/m-K}
    2000,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.2,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Alvenaria_2_4_Tijolo,    !- Name
    Rough,                   !- Roughness
    0.09,                    !- Thickness {m}
    0.9,                     !- Conductivity {W/m-K}
    1700,                    !- Density {kg/m3}
    920,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Alvenaria_3_Isolante,    !- Name
    MediumSmooth,            !- Roughness
    0.04,                    !- Thickness {m}
    0.035,                   !- Conductivity {W/m-K}
    130,                     !- Density {kg/m3}
    100,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Cobertura_1_Cascalho,    !- Name
    VeryRough,               !- Roughness
    0.01,                    !- Thickness {m}
    0.96,                    !- Conductivity {W/m-K}
    1800,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.5,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Cobertura_2_Impermeabilizante,  !- Name
    Rough,                   !- Roughness
    0.005,                   !- Thickness {m}
    0.5,                     !- Conductivity {W/m-K}
    1700,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Cobertura_3_Concreto,    !- Name
    MediumRough,             !- Roughness
    0.5,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2000,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.2,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Laje_1_concreto,         !- Name
    MediumSmooth,            !- Roughness
    0.13,                    !- Thickness {m}
    1.4,                     !- Conductivity {W/m-K}
    2100,                    !- Density {kg/m3}
    840,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.2,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_1_Argila,           !- Name
    Rough,                   !- Roughness
    0.75,                    !- Thickness {m}
    1.41,                    !- Conductivity {W/m-K}
    1900,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_2_Alvenaria,        !- Name
    VeryRough,               !- Roughness
    0.25,                    !- Thickness {m}
    0.84,                    !- Conductivity {W/m-K}
    1700,                    !- Density {kg/m3}
    800,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_3_Concreto,         !- Name
    Rough,                   !- Roughness
    1,                       !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2000,                    !- Density {kg/m3}
    1000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_4_Isolante,         !- Name
    MediumRough,             !- Roughness
    0.5,                     !- Thickness {m}
    0.025,                   !- Conductivity {W/m-K}
    30,                      !- Density {kg/m3}
    8000,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_5_Aglomerado,       !- Name
    MediumRough,             !- Roughness
    0.5,                     !- Thickness {m}
    0.15,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    160,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    Piso_6_Revestimento,     !- Name
    Smooth,                  !- Roughness
    0.1,                     !- Thickness {m}
    0.1,                     !- Conductivity {W/m-K}
    0.1,                     !- Density {kg/m3}
    700,                     !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

  Material,
    CHAPA METALICA,          !- Name
    VerySmooth,              !- Roughness
    0.005,                   !- Thickness {m}
    230,                     !- Conductivity {W/m-K}
    2700,                    !- Density {kg/m3}
    460,                     !- Specific Heat {J/kg-K}
    0.15,                    !- Thermal Absorptance
    0.7,                     !- Solar Absorptance
    0.7;                     !- Visible Absorptance

!-   ===========  ALL OBJECTS IN CLASS: MATERIAL:AIRGAP ===========

  Material:AirGap,
    Ar1,                     !- Name
    0.14;                    !- Thermal Resistance {m2-K/W}

  Material:AirGap,
    Ar2,                     !- Name
    0.61;                    !- Thermal Resistance {m2-K/W}

!-   ===========  ALL OBJECTS IN CLASS: WINDOWMATERIAL:GLAZING ===========

  WindowMaterial:Glazing,
    Clear 3mm,               !- Name
    SpectralAverage,         !- Optical Data Type
    ,                        !- Window Glass Spectral Data Set Name
    0.012,                   !- Thickness {m}
    0.837,                   !- Solar Transmittance at Normal Incidence
    0.075,                   !- Front Side Solar Reflectance at Normal Incidence
    0.075,                   !- Back Side Solar Reflectance at Normal Incidence
    0.898,                   !- Visible Transmittance at Normal Incidence
    0.081,                   !- Front Side Visible Reflectance at Normal Incidence
    0.081,                   !- Back Side Visible Reflectance at Normal Incidence
    0,                       !- Infrared Transmittance at Normal Incidence
    0.84,                    !- Front Side Infrared Hemispherical Emissivity
    0.84,                    !- Back Side Infrared Hemispherical Emissivity
    0.9;                     !- Conductivity {W/m-K}

!-   ===========  ALL OBJECTS IN CLASS: WINDOWMATERIAL:GAS ===========

  WindowMaterial:Gas,
    Air 13mm,                !- Name
    Air,                     !- Gas Type
    0.0127;                  !- Thickness {m}

!-   ===========  ALL OBJECTS IN CLASS: CONSTRUCTION ===========

  Construction,
    Alvenaria,               !- Name
    Alvenaria_1_5_Argamassa, !- Outside Layer
    Alvenaria_2_4_Tijolo,    !- Layer 2
    Alvenaria_3_Isolante,    !- Layer 3
    Alvenaria_2_4_Tijolo,    !- Layer 4
    Alvenaria_1_5_Argamassa; !- Layer 5

  Construction,
    Cobertura,               !- Name
    Cobertura_1_Cascalho,    !- Outside Layer
    Cobertura_2_Impermeabilizante,  !- Layer 2
    Cobertura_3_Concreto;    !- Layer 3

  Construction,
    Laje,                    !- Name
    Laje_1_concreto;         !- Outside Layer

  Construction,
    Vidro 6mm,               !- Name
    Clear 3mm;               !- Outside Layer

  Construction,
    CHAPA,                   !- Name
    Alvenaria_2_4_Tijolo;    !- Outside Layer

!-   ===========  ALL OBJECTS IN CLASS: GLOBALGEOMETRYRULES ===========

  GlobalGeometryRules,
    UpperLeftCorner,         !- Starting Vertex Position
    Counterclockwise,        !- Vertex Entry Direction
    Relative;                !- Coordinate System

!-   ===========  ALL OBJECTS IN CLASS: ZONE ===========

  Zone,
    PAV1_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    0.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV1_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    0.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV1_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    0.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV2_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    3.5,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV2_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    3.5,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV2_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    3.5,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV3_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    7.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV3_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    7.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV3_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    7.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV4_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    10.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV4_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    10.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV4_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    10.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV5_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    14.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV5_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    14.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV5_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    14.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV6_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    17.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV6_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    17.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV6_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    17.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV7_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    21.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV7_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    21.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV7_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    21.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV8_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    24.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV8_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    24.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV8_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    24.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV9_ZLAT2,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    42.0,                    !- X Origin {m}
    16.0,                    !- Y Origin {m}
    28.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV9_Z1,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    16.0,                    !- Y Origin {m}
    28.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV9_ZLAT1,              !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    16.0,                    !- Y Origin {m}
    28.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV10_ZLAT1,             !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    31.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV10_Z1,                !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    31.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV10_ZLAT2,             !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    31.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV11_ZLAT1,             !- Name
    0.0,                     !- Direction of Relative North {deg}
    -3.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    35.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV11_Z1,                !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    35.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV11_ZLAT2,             !- Name
    0.0,                     !- Direction of Relative North {deg}
    39.0,                    !- X Origin {m}
    0.0,                     !- Y Origin {m}
    35.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV2_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    3.5,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV3_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    7.0,                     !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV4_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    10.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV5_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    14.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV6_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    17.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV7_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    21.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV8_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    24.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV9_FD,                 !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    28.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV10_FD,                !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    31.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV11_FD,                !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    35.0,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

  Zone,
    PAV12_FD,                !- Name
    0.0,                     !- Direction of Relative North {deg}
    0.0,                     !- X Origin {m}
    0.0,                     !- Y Origin {m}
    38.5,                    !- Z Origin {m}
    ,                        !- Type
    1;                       !- Multiplier

!-   ===========  ALL OBJECTS IN CLASS: BUILDINGSURFACE:DETAILED ===========

  BuildingSurface:Detailed,
    PAV1_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Ground,                  !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV1_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Ground,                  !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Ground,                  !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV1_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV1_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV2_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV1_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT1_P3,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV3_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV7_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV7_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_ZLAT2_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_ZLAT1_PISO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_Z1_PISO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Ground,                  !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_Z1_P4,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT2_PISO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT2_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT2,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_PISO,            !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -39.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -39.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_ZLAT2_P2,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_P1,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_FD_P3,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -39.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -39.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_ZLAT1_P4,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -39.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -39.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_Z1_TETO,            !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV9_Z1,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_Z1_PISO,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    -39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -39.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_PISO,         !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_TETO,         !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT1_PISO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_P3,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_P2,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    -3.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_P1,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    -3.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    -3.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,-16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_ZLAT1_P4,           !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_ZLAT1,              !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_Z1_P2,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,-16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,-16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_PISO,        !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_ZLAT1_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_TETO,        !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_ZLAT1_PISO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_P2,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_P3,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_P1,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT1_P4,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT1,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_Z1_P2,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_PISO,           !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV10_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_Z1_TETO,            !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_P2,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT1_P4,          !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_P1,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_FD_P3,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_TETO,           !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV10_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_Z1_PISO,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_P3,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_Z1,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_Z1_P4,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT2_P2,          !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_PISO,        !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_ZLAT2_TETO,         !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_P2,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_Z1_P4,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_P4,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_P1,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_P3,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_ZLAT2_TETO,        !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV10_ZLAT2,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_ZLAT2_PISO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_PISO,        !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT1_TETO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_P3,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_P1,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_P2,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_TETO,        !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT1_P4,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT1,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_Z1_P2,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_PISO,           !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV11_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_Z1_TETO,           !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_P2,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_ZLAT1_P4,          !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_P1,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_FD_P3,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_P3,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_Z1,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_P4,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_Z1,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_ZLAT2_P2,          !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_Z1_TETO,           !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV11_Z1,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_PISO,        !- Name
    Floor,                   !- Surface Type
    Laje,                    !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_ZLAT2_TETO,        !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_P1,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_TETO,        !- Name
    Ceiling,                 !- Surface Type
    Laje,                    !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_P2,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_Z1_P4,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_P4,          !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    3.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_ZLAT2_P3,          !- Name
    Wall,                    !- Surface Type
    Cobertura,               !- Construction Name
    PAV11_ZLAT2,             !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    3.000000000000,16.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    3.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,16.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,16.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV2_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV2_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV2_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV4_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV3_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV4_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV4_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV6_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV5_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV6_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV6_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV8_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV8_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV8_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV7_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_P3,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_Z1_P1,              !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_P4,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV9_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_FD_PISO_CHAPA,     !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV9_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_P2,              !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV9_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_P3,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_Z1_P1,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_P2,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_TETO_CHAPA,     !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV10_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_FD_PISO_CHAPA,     !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_P4,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV10_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_PISO_CHAPA,     !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV10_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV9_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_P3,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_Z1_P1,             !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_P4,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_TETO_CHAPA,     !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV11_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV12_FD_PISO_CHAPA,     !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_PISO_CHAPA,     !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV11_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV10_FD_TETO_CHAPA,     !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_P2,             !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV11_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_PISO_CHAPA,     !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV11_FD_TETO_CHAPA,     !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_P4,             !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_TETO_CHAPA,     !- Name
    Roof,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_P2,             !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_P3,             !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV2_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV2_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    9D9851,                  !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV3_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV3_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV3_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV2_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV3_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV3_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV4_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV4_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV5_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    170237,                  !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV5_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV4_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    939E77,                  !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV5_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV5_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV5_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV6_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV6_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_FD_PISO_CHAPA,      !- Name
    Floor,                   !- Surface Type
    CHAPA,                   !- Construction Name
    PAV7_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV6_FD_TETO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,0.000000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_FD_TETO_CHAPA,      !- Name
    Ceiling,                 !- Surface Type
    CHAPA,                   !- Construction Name
    PAV7_FD,                 !- Zone Name
    Surface,                 !- Outside Boundary Condition
    PAV8_FD_PISO_CHAPA,      !- Outside Boundary Condition Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV7_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV7_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    5A1156,                  !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,0.000000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    AAAA7D,                  !- Name
    Wall,                    !- Surface Type
    Alvenaria,               !- Construction Name
    PAV7_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,0.000000000000,0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,0.000000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV8_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV8_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV9_FD_P1_CHAPA,        !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV9_FD,                 !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV10_FD_P1_CHAPA,       !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV10_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV11_FD_P1_CHAPA,       !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV11_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  BuildingSurface:Detailed,
    PAV12_FD_P1_CHAPA,       !- Name
    Wall,                    !- Surface Type
    CHAPA,                   !- Construction Name
    PAV12_FD,                !- Zone Name
    Outdoors,                !- Outside Boundary Condition
    ,                        !- Outside Boundary Condition Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    ,                        !- View Factor to Ground
    4,                       !- Number of Vertices
    0.000000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    39.000000000000,'''+str(-0.4-x[0])+''',3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

!-   ===========  ALL OBJECTS IN CLASS: FENESTRATIONSURFACE:DETAILED ===========

  FenestrationSurface:Detailed,
    PAV2_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_Z1_P1,              !- Building Surface Name
    PAV2_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV2_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV1_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV1_Z1_P1,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,3.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,2.050000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,2.050000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,3.000000000000;  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV1_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV1_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,1.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,0.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,0.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,1.500000000000;  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV3_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_Z1_P1,              !- Building Surface Name
    PAV3_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV3_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV4_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_Z1_P1,              !- Building Surface Name
    PAV4_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV4_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV5_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_Z1_P1,              !- Building Surface Name
    PAV5_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV5_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV6_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_Z1_P1,              !- Building Surface Name
    PAV6_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV6_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV7_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_Z1_P1,              !- Building Surface Name
    PAV7_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV7_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV8_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_Z1_P1,              !- Building Surface Name
    PAV8_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV8_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV9_Z1_P3_J1_VENEZIANA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_Z1_P3,              !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    -0.200000000000,0.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    -0.200000000000,0.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    -38.800000000000,0.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    -38.800000000000,0.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV9_Z1_P1_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_Z1_P1,              !- Building Surface Name
    PAV9_FD_P3_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    -38.800000000000,-16.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    -38.800000000000,-16.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    -0.200000000000,-16.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    -0.200000000000,-16.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV10_Z1_P1_J2_ABRE,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_Z1_P1,             !- Building Surface Name
    PAV10_FD_P3_J2_ABRE,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV10_Z1_P3_J1_VENEZIANA,!- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_Z1_P3,             !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV11_Z1_P1_J2_ABRE,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_Z1_P1,             !- Building Surface Name
    PAV11_FD_P3_J2_ABRE,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV11_Z1_P3_J1_VENEZIANA,!- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_Z1_P3,             !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,16.000000000000,'''+str(1.525-(x[3]/2.0)+x[6])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,16.000000000000,'''+str(2.475+(x[3]/2.0)+x[6])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV2_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_FD_P3,              !- Building Surface Name
    PAV2_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV3_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_FD_P3,              !- Building Surface Name
    PAV3_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV4_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_FD_P3,              !- Building Surface Name
    PAV4_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV5_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_FD_P3,              !- Building Surface Name
    PAV5_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV6_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_FD_P3,              !- Building Surface Name
    PAV6_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV7_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_FD_P3,              !- Building Surface Name
    PAV7_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV8_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_FD_P3,              !- Building Surface Name
    PAV8_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV9_FD_P3_J2_ABRE,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_FD_P3,              !- Building Surface Name
    PAV9_Z1_P1_J2_ABRE,      !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV10_FD_P3_J2_ABRE,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_FD_P3,             !- Building Surface Name
    PAV10_Z1_P1_J2_ABRE,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV11_FD_P3_J2_ABRE,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_FD_P3,             !- Building Surface Name
    PAV11_Z1_P1_J2_ABRE,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.800000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 1 {m}
    38.800000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 2 {m}
    0.200000000000,0.000000000000,'''+str(1.525-(x[4]/2.0)+x[5])+''',  !- X,Y,Z ==> Vertex 3 {m}
    0.200000000000,0.000000000000,'''+str(2.475+(x[4]/2.0)+x[5])+''';  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV2_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV2_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_FD_TETO_CHAPA,      !- Building Surface Name
    PAV3_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV3_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV4_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV5_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV4_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_FD_TETO_CHAPA,      !- Building Surface Name
    PAV5_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV3_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_FD_PISO_CHAPA,      !- Building Surface Name
    PAV2_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV3_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV3_FD_TETO_CHAPA,      !- Building Surface Name
    PAV4_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}
    
    FenestrationSurface:Detailed,
    PAV2_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV2_FD_PISO_CHAPA,      !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}


  FenestrationSurface:Detailed,
    PAV5_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_FD_TETO_CHAPA,      !- Building Surface Name
    PAV6_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV6_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV8_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV9_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV10_FD_P1_J1_FIXO,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_FD_P1_CHAPA,       !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV11_FD_P1_J1_FIXO,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_FD_P1_CHAPA,       !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV12_FD_P1_J1_FIXO,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV12_FD_P1_CHAPA,       !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV11_FD_TETO_ABERTA,    !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_FD_TETO_CHAPA,     !- Building Surface Name
    PAV12_FD_PISO_J1_ABERTA, !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV11_FD_PISO_J1_ABERTA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV11_FD_PISO_CHAPA,     !- Building Surface Name
    PAV10_FD_TETO_ABERTA,    !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV10_FD_TETO_ABERTA,    !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_FD_TETO_CHAPA,     !- Building Surface Name
    PAV11_FD_PISO_J1_ABERTA, !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV10_FD_PISO_J1_ABERTA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV10_FD_PISO_CHAPA,     !- Building Surface Name
    PAV9_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV9_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_FD_TETO_CHAPA,      !- Building Surface Name
    PAV10_FD_PISO_J1_ABERTA, !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV9_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV9_FD_PISO_CHAPA,      !- Building Surface Name
    PAV8_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV7_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_FD_TETO_CHAPA,      !- Building Surface Name
    PAV8_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV8_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_FD_PISO_CHAPA,      !- Building Surface Name
    PAV7_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV8_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV8_FD_TETO_CHAPA,      !- Building Surface Name
    PAV9_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV7_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_FD_PISO_CHAPA,      !- Building Surface Name
    PAV6_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV7_FD_P1_J1_FIXO,      !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV7_FD_P1_CHAPA,        !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.900000000000,'''+str(-0.4-x[0])+''',3.400021581812,  !- X,Y,Z ==> Vertex 1 {m}
    38.900000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 2 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',0.099978418188,  !- X,Y,Z ==> Vertex 3 {m}
    0.100000000000,'''+str(-0.4-x[0])+''',3.400021581812;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV5_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV5_FD_PISO_CHAPA,      !- Building Surface Name
    PAV4_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV4_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV4_FD_PISO_CHAPA,      !- Building Surface Name
    PAV3_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV12_FD_PISO_J1_ABERTA, !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV12_FD_PISO_CHAPA,     !- Building Surface Name
    PAV11_FD_TETO_ABERTA,    !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV6_FD_PISO_J1_ABERTA,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_FD_PISO_CHAPA,      !- Building Surface Name
    PAV5_FD_TETO_ABERTA,     !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    38.990000000000,-0.010000000000,0.000000000000,  !- X,Y,Z ==> Vertex 1 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 2 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',0.000000000000,  !- X,Y,Z ==> Vertex 3 {m}
    0.010000000000,-0.010000000000,0.000000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV12_FD_TETO_ABERTA_FINAL,  !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV12_FD_TETO_CHAPA,     !- Building Surface Name
    ,                        !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

  FenestrationSurface:Detailed,
    PAV6_FD_TETO_ABERTA,     !- Name
    Window,                  !- Surface Type
    Vidro 6mm,               !- Construction Name
    PAV6_FD_TETO_CHAPA,      !- Building Surface Name
    PAV7_FD_PISO_J1_ABERTA,  !- Outside Boundary Condition Object
    ,                        !- View Factor to Ground
    ,                        !- Frame and Divider Name
    ,                        !- Multiplier
    4,                       !- Number of Vertices
    0.010000000000,-0.010000000000,3.500000000000,  !- X,Y,Z ==> Vertex 1 {m}
    0.010000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 2 {m}
    38.990000000000,'''+str(-0.4-x[0])+''',3.500000000000,  !- X,Y,Z ==> Vertex 3 {m}
    38.990000000000,-0.010000000000,3.500000000000;  !- X,Y,Z ==> Vertex 4 {m}

!-   ===========  ALL OBJECTS IN CLASS: PEOPLE ===========

  People,
    Trabalhadores_PAV1,      !- Name
    PAV1_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV2,      !- Name
    PAV2_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV3,      !- Name
    PAV3_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV4,      !- Name
    PAV4_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV5,      !- Name
    PAV5_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV6,      !- Name
    PAV6_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV7,      !- Name
    PAV7_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV8,      !- Name
    PAV8_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV9,      !- Name
    PAV9_Z1,                 !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV10,     !- Name
    PAV10_Z1,                !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

  People,
    Trabalhadores_PAV11,     !- Name
    PAV11_Z1,                !- Zone or ZoneList Name
    Ocupacao,                !- Number of People Schedule Name
    People,                  !- Number of People Calculation Method
    45,                      !- Number of People
    ,                        !- People per Zone Floor Area {person/m2}
    ,                        !- Zone Floor Area per Person {m2/person}
    0.6,                     !- Fraction Radiant
    autocalculate,           !- Sensible Heat Fraction
    metabolismo_esc,         !- Activity Level Schedule Name
    0.0000000382,            !- Carbon Dioxide Generation Rate {m3/s-W}
    No,                      !- Enable ASHRAE 55 Comfort Warnings
    ZoneAveraged,            !- Mean Radiant Temperature Calculation Type
    ,                        !- Surface Name/Angle Factor List Name
    ,                        !- Work Efficiency Schedule Name
    ClothingInsulationSchedule;  !- Clothing Insulation Calculation Method

!-   ===========  ALL OBJECTS IN CLASS: LIGHTS ===========

  Lights,
    Iluminacao_PAV1,         !- Name
    PAV1_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV2,         !- Name
    PAV2_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV3,         !- Name
    PAV3_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV4,         !- Name
    PAV4_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV5,         !- Name
    PAV5_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV6,         !- Name
    PAV6_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV7,         !- Name
    PAV7_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV8,         !- Name
    PAV8_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV9,         !- Name
    PAV9_Z1,                 !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV10,        !- Name
    PAV10_Z1,                !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

  Lights,
    Iluminacao_PAV11,        !- Name
    PAV11_Z1,                !- Zone or ZoneList Name
    Ilum_Total,              !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Lighting Level {W}
    18.75,                   !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Return Air Fraction
    0.72,                    !- Fraction Radiant
    0.18,                    !- Fraction Visible
    1,                       !- Fraction Replaceable
    General,                 !- End-Use Subcategory
    No;                      !- Return Air Fraction Calculated from Plenum Temperature

!-   ===========  ALL OBJECTS IN CLASS: ELECTRICEQUIPMENT ===========

  ElectricEquipment,
    Equipamento_PAV1,        !- Name
    PAV1_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV2,        !- Name
    PAV2_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV3,        !- Name
    PAV3_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV4,        !- Name
    PAV4_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV5,        !- Name
    PAV5_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV6,        !- Name
    PAV6_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV7,        !- Name
    PAV7_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV8,        !- Name
    PAV8_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV9,        !- Name
    PAV9_Z1,                 !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV10,       !- Name
    PAV10_Z1,                !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

  ElectricEquipment,
    Equipamento_PAV11,       !- Name
    PAV11_Z1,                !- Zone or ZoneList Name
    Equip_esc,               !- Schedule Name
    Watts/Area,              !- Design Level Calculation Method
    ,                        !- Design Level {W}
    8.4,                     !- Watts per Zone Floor Area {W/m2}
    ,                        !- Watts per Person {W/person}
    0,                       !- Fraction Latent
    0.3,                     !- Fraction Radiant
    0,                       !- Fraction Lost
    General;                 !- End-Use Subcategory

!-   ===========  ALL OBJECTS IN CLASS: AIRFLOWNETWORK:SIMULATIONCONTROL ===========

  AirflowNetwork:SimulationControl,
    Ventilacao_Nat,          !- Name
    MultizoneWithoutDistribution,  !- AirflowNetwork Control
    SurfaceAverageCalculation,  !- Wind Pressure Coefficient Type
    ,                        !- Height Selection for Local Wind Pressure Calculation
    LowRise,                 !- Building Type
    500,                     !- Maximum Number of Iterations {dimensionless}
    ZeroNodePressures,       !- Initialization Type
    0.0001,                  !- Relative Airflow Convergence Tolerance {dimensionless}
    0.000001,                !- Absolute Airflow Convergence Tolerance {kg/s}
    -.5,                     !- Convergence Acceleration Limit {dimensionless}
    90,                      !- Azimuth Angle of Long Axis of Building {deg}
    1,                       !- Ratio of Building Width Along Short Axis to Width Along Long Axis
    No;                      !- Height Dependence of External Node Temperature

!-   ===========  ALL OBJECTS IN CLASS: AIRFLOWNETWORK:MULTIZONE:ZONE ===========

  AirflowNetwork:MultiZone:Zone,
    PAV1_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV2_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV3_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV4_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV5_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV6_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV7_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV8_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV9_Z1,                 !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV10_Z1,                !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV11_Z1,                !- Zone Name
    Temperature,             !- Ventilation Control Mode
    AberturaJanelas,         !- Ventilation Control Zone Temperature Setpoint Schedule Name
    0.33,                    !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    ,                        !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV2_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV3_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV4_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV5_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV6_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV7_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV8_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV9_FD,                 !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV10_FD,                !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV11_FD,                !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

  AirflowNetwork:MultiZone:Zone,
    PAV12_FD,                !- Zone Name
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    1,                       !- Minimum Venting Open Factor {dimensionless}
    0,                       !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    6,                       !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    0,                       !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000,                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    Always On,               !- Venting Availability Schedule Name
    Standard,                !- Single Sided Wind Pressure Coefficient Algorithm
    10;                      !- Facade Width {m}

!-   ===========  ALL OBJECTS IN CLASS: AIRFLOWNETWORK:MULTIZONE:SURFACE ===========

  AirflowNetwork:MultiZone:Surface,
    PAV11_FD_PISO_J1_ABERTA, !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV11_FD_TETO_ABERTA,    !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV10_FD_PISO_J1_ABERTA, !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV10_FD_TETO_ABERTA,    !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV9_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV9_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV8_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV8_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV7_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV7_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV6_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV6_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV5_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV5_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV4_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV4_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV3_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV3_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV2_FD_PISO_J1_ABERTA,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[9])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
  

  AirflowNetwork:MultiZone:Surface,
    PAV2_FD_TETO_ABERTA,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV11_FD_P1_J1_FIXO,     !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV10_FD_P1_J1_FIXO,     !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV9_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV8_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV7_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV6_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV5_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV4_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV3_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}


  AirflowNetwork:MultiZone:Surface,
    PAV2_FD_P1_J1_FIXO,      !- Surface Name
    fixo,                    !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always Off,              !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV11_FD_P3_J2_ABRE,     !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV10_FD_P3_J2_ABRE,     !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV9_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV8_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV7_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV6_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV5_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV4_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV3_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV2_FD_P3_J2_ABRE,      !- Surface Name
    correr,                  !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}
    
  AirflowNetwork:MultiZone:Surface,
    PAV1_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}



  AirflowNetwork:MultiZone:Surface,
    PAV1_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV2_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV3_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV4_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV5_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV6_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV7_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV8_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV9_Z1_P3_J1_VENEZIANA, !- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV10_Z1_P3_J1_VENEZIANA,!- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV11_Z1_P3_J1_VENEZIANA,!- Surface Name
    Veneziana,               !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[8])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV11_Z1_P1_J2_ABRE,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV10_Z1_P1_J2_ABRE,     !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV9_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV8_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV7_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV6_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV5_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV4_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV3_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV2_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[7])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV1_Z1_P1_J2_ABRE,      !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    ZoneLevel,               !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV12_FD_PISO_J1_ABERTA, !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    1,                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

  AirflowNetwork:MultiZone:Surface,
    PAV12_FD_TETO_ABERTA_FINAL,  !- Surface Name
    vao,                     !- Leakage Component Name
    ,                        !- External Node Name
    '''+str(x[1])+''',                       !- Window/Door Opening Factor, or Crack Factor {dimensionless}
    Constant,                !- Ventilation Control Mode
    Always On,               !- Ventilation Control Zone Temperature Setpoint Schedule Name
    ,                        !- Minimum Venting Open Factor {dimensionless}
    ,                        !- Indoor and Outdoor Temperature Difference Lower Limit For Maximum Venting Open Factor {deltaC}
    100,                     !- Indoor and Outdoor Temperature Difference Upper Limit for Minimum Venting Open Factor {deltaC}
    ,                        !- Indoor and Outdoor Enthalpy Difference Lower Limit For Maximum Venting Open Factor {deltaJ/kg}
    300000;                  !- Indoor and Outdoor Enthalpy Difference Upper Limit for Minimum Venting Open Factor {deltaJ/kg}

!-   ===========  ALL OBJECTS IN CLASS: AIRFLOWNETWORK:MULTIZONE:COMPONENT:DETAILEDOPENING ===========

  AirflowNetwork:MultiZone:Component:DetailedOpening,
    fixo,                    !- Name
    0.001,                   !- Air Mass Flow Coefficient When Opening is Closed {kg/s-m}
    0.65,                    !- Air Mass Flow Exponent When Opening is Closed {dimensionless}
    NonPivoted,              !- Type of Rectangular Large Vertical Opening (LVO)
    ,                        !- Extra Crack Length or Height of Pivoting Axis {m}
    2,                       !- Number of Sets of Opening Factor Data
    0,                       !- Opening Factor 1 {dimensionless}
    0.001,                   !- Discharge Coefficient for Opening Factor 1 {dimensionless}
    0,                       !- Width Factor for Opening Factor 1 {dimensionless}
    0,                       !- Height Factor for Opening Factor 1 {dimensionless}
    0,                       !- Start Height Factor for Opening Factor 1 {dimensionless}
    1,                       !- Opening Factor 2 {dimensionless}
    0.001,                   !- Discharge Coefficient for Opening Factor 2 {dimensionless}
    1,                       !- Width Factor for Opening Factor 2 {dimensionless}
    1,                       !- Height Factor for Opening Factor 2 {dimensionless}
    0;                       !- Start Height Factor for Opening Factor 2 {dimensionless}

  AirflowNetwork:MultiZone:Component:DetailedOpening,
    vao,                     !- Name
    0.001,                   !- Air Mass Flow Coefficient When Opening is Closed {kg/s-m}
    0.65,                    !- Air Mass Flow Exponent When Opening is Closed {dimensionless}
    NonPivoted,              !- Type of Rectangular Large Vertical Opening (LVO)
    ,                        !- Extra Crack Length or Height of Pivoting Axis {m}
    2,                       !- Number of Sets of Opening Factor Data
    0,                       !- Opening Factor 1 {dimensionless}
    0.65,                    !- Discharge Coefficient for Opening Factor 1 {dimensionless}
    0,                       !- Width Factor for Opening Factor 1 {dimensionless}
    0,                       !- Height Factor for Opening Factor 1 {dimensionless}
    0,                       !- Start Height Factor for Opening Factor 1 {dimensionless}
    1,                       !- Opening Factor 2 {dimensionless}
    0.65,                    !- Discharge Coefficient for Opening Factor 2 {dimensionless}
    1,                       !- Width Factor for Opening Factor 2 {dimensionless}
    1,                       !- Height Factor for Opening Factor 2 {dimensionless}
    ;                        !- Start Height Factor for Opening Factor 2 {dimensionless}

  AirflowNetwork:MultiZone:Component:DetailedOpening,
    Veneziana,               !- Name
    0.001,                   !- Air Mass Flow Coefficient When Opening is Closed {kg/s-m}
    0.65,                    !- Air Mass Flow Exponent When Opening is Closed {dimensionless}
    HorizontallyPivoted,     !- Type of Rectangular Large Vertical Opening (LVO)
    ,                        !- Extra Crack Length or Height of Pivoting Axis {m}
    2,                       !- Number of Sets of Opening Factor Data
    0,                       !- Opening Factor 1 {dimensionless}
    0.001,                   !- Discharge Coefficient for Opening Factor 1 {dimensionless}
    0,                       !- Width Factor for Opening Factor 1 {dimensionless}
    0,                       !- Height Factor for Opening Factor 1 {dimensionless}
    0,                       !- Start Height Factor for Opening Factor 1 {dimensionless}
    1,                       !- Opening Factor 2 {dimensionless}
    0.4,                     !- Discharge Coefficient for Opening Factor 2 {dimensionless}
    1,                       !- Width Factor for Opening Factor 2 {dimensionless}
    1,                       !- Height Factor for Opening Factor 2 {dimensionless}
    ;                        !- Start Height Factor for Opening Factor 2 {dimensionless}

  AirflowNetwork:MultiZone:Component:DetailedOpening,
    correr,                  !- Name
    0.001,                   !- Air Mass Flow Coefficient When Opening is Closed {kg/s-m}
    0.65,                    !- Air Mass Flow Exponent When Opening is Closed {dimensionless}
    NonPivoted,              !- Type of Rectangular Large Vertical Opening (LVO)
    ,                        !- Extra Crack Length or Height of Pivoting Axis {m}
    3,                       !- Number of Sets of Opening Factor Data
    0,                       !- Opening Factor 1 {dimensionless}
    0.001,                   !- Discharge Coefficient for Opening Factor 1 {dimensionless}
    0,                       !- Width Factor for Opening Factor 1 {dimensionless}
    0,                       !- Height Factor for Opening Factor 1 {dimensionless}
    0,                       !- Start Height Factor for Opening Factor 1 {dimensionless}
    0.5,                     !- Opening Factor 2 {dimensionless}
    0.6,                     !- Discharge Coefficient for Opening Factor 2 {dimensionless}
    0.225,                   !- Width Factor for Opening Factor 2 {dimensionless}
    0.9,                     !- Height Factor for Opening Factor 2 {dimensionless}
    0,                       !- Start Height Factor for Opening Factor 2 {dimensionless}
    1,                       !- Opening Factor 3 {dimensionless}
    0.6,                     !- Discharge Coefficient for Opening Factor 3 {dimensionless}
    0.45,                    !- Width Factor for Opening Factor 3 {dimensionless}
    0.9,                     !- Height Factor for Opening Factor 3 {dimensionless}
    0;                       !- Start Height Factor for Opening Factor 3 {dimensionless}

!-   ===========  ALL OBJECTS IN CLASS: HVACTEMPLATE:THERMOSTAT ===========

  HVACTemplate:Thermostat,
    Constant Setpoint Thermostat,  !- Name
    ,                        !- Heating Setpoint Schedule Name
    20,                      !- Constant Heating Setpoint {C}
    ,                        !- Cooling Setpoint Schedule Name
    25;                      !- Constant Cooling Setpoint {C}

!-   ===========  ALL OBJECTS IN CLASS: OUTPUT:VARIABLEDICTIONARY ===========

  Output:VariableDictionary,IDF;

!-   ===========  ALL OBJECTS IN CLASS: OUTPUT:VARIABLE ===========

  Output:Variable,*,Zone Mean Air Temperature,Hourly;

  Output:Variable,*,AFN Linkage Node 1 to Node 2 Volume Flow Rate,Hourly;

  Output:Variable,*,AFN Linkage Node 2 to Node 1 Volume Flow Rate,Hourly;

  Output:Variable,*,Zone Mean Radiant Temperature,Hourly;

  OutputControl:Table:Style,
    CommaAndHTML;                    !- Column Separator

  Output:Table:SummaryReports,
    AllSummary;              !- Report 1 Name

  Output:VariableDictionary,IDF,Unsorted;

  Output:SQLite,
    SimpleAndTabular;        !- Option Type

  LifeCycleCost:NonrecurringCost,
    Default Cost,            !- Name
    Construction,            !- Category
    0,                       !- Cost
    ServicePeriod;           !- Start of Costs

	'''
    return idf_file

'''
class _HTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'br') and not self.hide_output:
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p':
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r'\s+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = unichr(name2codepoint[name])
            self._buf.append(c)

    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._buf.append(unichr(n))

    def get_text(self):
        return re.sub(r' +', ' ', ''.join(self._buf))

def html_to_text(html):
    """
    Given a piece of HTML, return the plain text it contains.
    This handles entities and char refs, but not javascript and stylesheets.
    """
    parser = _HTMLToText()
    try:
        parser.feed(html)
        parser.close()
    except HTMLParseError:
        pass
    return parser.get_text()

def text_to_html(text):
    """
    Convert the given text to html, wrapping what looks like URLs with <a> tags,
    converting newlines to <br> tags and converting confusing chars into html
    entities.
    """
    def f(mo):
        t = mo.group()
        if len(t) == 1:
            return {'&':'&amp;', "'":'&#39;', '"':'&quot;', '<':'&lt;', '>':'&gt;'}.get(t)
        return '<a href="%s">%s</a>' % (t, t)
    return re.sub(r'https?://[^] ()"\';]+|[&\'"<>]', f, text)


def extract_limits(file_name):
    # Extract the acceptability limits to use as objective function parameters
    lookup = 'Acceptability'
    num_lines = []
    with open(file_name) as myFile:
        for num, line in enumerate(myFile, 1):
            if lookup in line:
                num_lines.append(num)
    
    line = open(file_name, "r").readlines()[num_lines[0]:num_lines[0]+38]
    limits = []

    for l in range(len(line)):   
        if l in [7,8,15,16,23,24,31,32]: # lines with the acceptability limits
            limits.append(float(html_to_text(line[l])))
    limits = np.array(limits).reshape(4,2)
    
    return limits   

def geometric_mean(limits):
    # geometric mean as objective function
    ninety_per = limits[:,0]
    eighty_per = limits[:,1]
    #print(eighty_per)
    s=stats.gmean(eighty_per)#*np.std(eighty_per)*np.max(eighty_per)
    return s, eighty_per
'''
    
def filtra_periodo(inicio, fim, df_):
    time = []
    horas = []
    for index, row in df_.iterrows():
        timestamp = row['Date/Time']
        sep1 = timestamp.split('/')
        date_time = sep1[1].split(' ')
        time.append(date_time[2])
        hora = date_time[2].split(':')
        horas.append(int(hora[0]))
    df_['Time'] = time
    df_['Hour'] = horas
    df2 = df_.loc[((df_['Hour']>=inicio) & (df_['Hour']<=fim))]
    return df2

'''
def run_idf_eighty_per(pwd,path,model):
    # Run a idf file return the objective function
    epw_file = pwd+'BRA_DF_Brasilia.867150_INMET.epw'
    #os.system("energyplus -w " + epw_file+' '+ model+" >> out_trash_EP.txt")
    os.system("energyplus -w " + epw_file+' -r -x '+ model+" > /dev/null")
    file_name = path+'eplustbl.htm'
    limits = extract_limits(file_name)
    mean, eighty_per = geometric_mean(limits)

    return mean, eighty_per 
'''

def run_idf_fluxo_topo(pwd, path, model):
    # Run a idf file return the objective function
    epw_file = pwd+'weather_files/BRA_DF_Brasilia.867150_INMET/BRA_DF_Brasilia.867150_INMET.epw'
    #os.system("energyplus -w " + epw_file+' '+ model+" >> out_trash_EP.txt")
    os.system("energyplus -w " + epw_file+' -r -x '+ model+" > /dev/null")
    file_name = path+'eplusout.csv'
    col_list= ['Date/Time','PAV11_FD_TETO_ABERTA:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](Hourly)','PAV11_FD_TETO_ABERTA:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](Hourly)',]
    df = pd.read_csv(file_name, usecols=col_list)
    df = df.rename(columns={'PAV12_FD_TETO_ABERTA_FINAL:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](Hourly)': 'PAV11_FD_TETO_ABERTA_1_2',
                            'PAV12_FD_TETO_ABERTA_FINAL:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](Hourly)': 'PAV11_FD_TETO_ABERTA_2_1'})
    df = filtra_periodo(8,18,df)    
    fluxo = df['PAV12_FD_TETO_ABERTA_FINAL_1_2']-df['PAV12_FD_TETO_ABERTA_FINAL_2_1']
    print('fluxo',fluxo.head())
    col_mean, col_max = fluxo.mean(), fluxo.max()
    col_mean = -1*col_mean
       
    return col_mean, col_max
    
def run_idf_fluxo_5_andar(pwd, path, model, weather_file_):
    # Run a idf file return the objective function
    epw_file = weather_file_ #pwd+'weather_files/BRA_DF_Brasilia.867150_INMET/BRA_DF_Brasilia.867150_INMET.epw'
    print("passou")
    #os.system("energyplus -w " + epw_file+' '+path+model+" >> out_trash_EP.txt")
    os.system("energyplus -w " + epw_file+' -r -x '+ path+model+" > /dev/null")
    #print("energyplus -w " + epw_file+' -r -x '+ path+model+" > /dev/null")

    #with subprocess.Popen("energyplus -w " + epw_file+' -r -x '+pwd+model+" > /dev/null") as p: p.wait()
    #os.system('energyplus -w ./weather_files/Z5_PARATY-RJ_proj_2100.epw -r -x fachada_dupla.idf >> texto.txt; sleep 10')
    #subprocess.run('energyplus -w weather_files/Z5_PARATY-RJ_proj_2100.epw -r -x fachada_dupla.idf > /dev/null')
    
    file_name = 'eplusout.csv'
    col_list= ['Date/Time','PAV5_FD_P3_J2_ABRE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](Hourly)','PAV5_FD_P3_J2_ABRE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](Hourly)']
    df = pd.read_csv(file_name, usecols=col_list)
    df = df.rename(columns={'PAV5_FD_P3_J2_ABRE:AFN Linkage Node 1 to Node 2 Volume Flow Rate [m3/s](Hourly)': 'PAV5_FD_P3_J2_ABRE_1_2',
                            'PAV5_FD_P3_J2_ABRE:AFN Linkage Node 2 to Node 1 Volume Flow Rate [m3/s](Hourly)': 'PAV5_FD_P3_J2_ABRE_2_1'})
    df = filtra_periodo(8,18,df)
    fluxo = df['PAV5_FD_P3_J2_ABRE_2_1']-df['PAV5_FD_P3_J2_ABRE_1_2']
    col_mean, col_max = fluxo.mean(), fluxo.max()
    col_mean = -1*col_mean
    
    
    return col_mean, col_max
    
def objective_function(x,weather):
    pwd=os.getcwd()+'/'
    # Reads a idf file and evaluate the objective function
    idf_file = gen_idf(x) 
    os.system('mkdir ./tmp')
    aux=str(int(time.time()*1e16))
    path='./tmp/'+aux+'/'
    os.system('mkdir '+path)
    #out_file = path+"fachada_dupla_remove_"+aux+".idf"
    out_file = "fachada_dupla.idf"
    with open(path+out_file, "w") as text_file:
        text_file.write(idf_file)
    
    #os.chdir(path)
    f_, g_= run_idf_fluxo_5_andar(pwd,path,out_file, weather)
    #os.chdir(pwd)
    print('col_mean:',f_,'    x:',x)
    os.system('rm -rf '+path)
    return f_,g_

# Materials ans parameters

def obj_fun(x0, weather_file, flag=0):
    x=np.round(x0).astype(int)
    
    #azimuth = [0, 45, 90, 135, 180, 225, 270, 315]
        
    larg_cavid = [0.55,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0.0]
    aber_cavid_sup = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    rotacao = [0,45,90,135,180,225,270]
    delta_janelas_tras = [0,0.1,0.2,0.3,0.4]
    delta_janelas_frente = [0,0.1,0.2,0.3,0.4]
    mov_janelas_frente = [-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    mov_janelas_tras = [-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
    aber_janelas_frente = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    aber_janelas_tras = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    aber_base_fachada = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    
    
    x = [larg_cavid[x[0]],aber_cavid_sup[x[1]],rotacao[x[2]],delta_janelas_tras[x[3]],delta_janelas_frente[x[4]],mov_janelas_frente[x[5]], mov_janelas_tras[x[6]],aber_janelas_frente[x[7]],aber_janelas_tras[x[8]],aber_base_fachada[x[9]]]
    f,g= objective_function(x, weather_file)
    print('obj_fun   ','x: ',x ,'f: ',f)
    #f,g= np.dot(x0,x0)+np.random.rand(), np.sum(x0)
    #print('--',f,g)
    return f if flag==0 else (f,g)

class fachada_dupla:
    def __init__(self, weather_file):
         self.lb=[0,0,0,0,0,0,0,0,0,0]    
         self.ub=[10,9,6,4,4,16,16,9,9,9]
         self.dim = len(self.lb)
         self.weather_file = weather_file
         
    def fitness(self, x, flag=0):
         return [obj_fun(x, self.weather_file, flag)]
        
    def get_bounds(self):
         return (self.lb,self.ub)
    
    def get_name(self):         
         return "Fachada Dupla"

    def get_extra_info(self):
         return "\tDimensions: " + str(self.dim)


#============================================================================================================================

arquivos_cidades=[['Z5 PARATY-RJ','INMET_SE_RJ_A619_PARATY_01-01-2022_A_31-12-2022.CSV', 'BRA_RJ_Paraty.869130_INMET','CABra_375'], 
['Z3 JUIZ DE FORA-MG','INMET_SE_MG_A518_JUIZ DE FORA_01-01-2022_A_31-12-2022.CSV', 'BRA_MG_Juiz.de.Fora.836920_INMET','CABra_331'], 
['Z8 VALENCA-BA','INMET_NE_BA_A444_VALENCA_01-01-2022_A_31-12-2022.CSV', 'BRA_BA_Valenca.866760_INMET','CABra_226'],
['Z6 BRASILIA-DF', 'INMET_CO_DF_A001_BRASILIA_01-01-2022_A_31-12-2022.CSV', 'BRA_DF_Brasilia.867150_INMET','CABra_698'],
['Z1 CURITIBA-PR','INMET_S_PR_A807_CURITIBA_01-01-2022_A_31-12-2022.CSV','BRA_PR_Curitiba.838420_INMET','CABra_717'], 
['Z2 SANTA MARIA-RS','INMET_S_RS_A803_SANTA MARIA_01-01-2022_A_31-12-2022.CSV','BRA_RS_Santa.Maria.839360_INMET','CABra_598'], 
['Z4 UBERLANDIA-MG','INMET_SE_MG_A507_UBERLANDIA_01-01-2022_A_31-12-2022.CSV','BRA_MG_Uberlandia.867760_INMET','CABra_387'], 
['Z7 BOM JESUS DO PIAUI-PI','INMET_NE_PI_A326_BOM JESUS DO PIAUI_01-01-2022_A_31-12-2022.CSV','BRA_PI_Bom.Jesus.do.Piaui.829750_INMET','CABra_128'], 
['Z8 MANAUS-AM','INMET_N_AM_A101_MANAUS_01-01-2022_A_31-12-2022.CSV','BRA_AM_Manaus-Gomez.Intl.AP.817300_INMET','CABra_15']]

#path_weather_files = './weather_files/'+arquivos_cidades[0][0]
#weather_file = path_weather_files+'_proj_2100.epw'
weather_file = './weather_files/Z5_PARATY-RJ_proj_2100.epw'


basename='fachada_dupla_paraty_2100_'
os.system('mkdir ./pkl')
path='./pkl/'

if len (sys.argv) == 1 :
    run=0
elif len (sys.argv) == 3 :
    run = int(sys.argv[2]) if sys.argv[1]=='-r' else None
else:    
    print("Usage: python  "+ sys.argv[0]+' -r N')
    sys.exit (1)

file_tempo = 'fachada_dupla_ga_paraty_2100.txt'
s_tempo = ''

obj=fachada_dupla(weather_file)
prob = pg.problem(obj)


udas=[
        #pg.de(gen = 1, seed = 0),
        #pg.sea(gen = pop_size, seed = 0),
        pg.sga(gen = 1, m=0.3, seed = 0),
        #pg.sga_gray(gen=1,cr=0.95, m=0.02, elitism=1)
        #pg.ihs(gen = 1, seed = 0),
        #pg.pso(gen = 1, memory=True, seed = 0),
        #pg.bee_colony(gen = 50, limit = 5, seed = 0),
        
    ]

run=1
maxgen=50
pop_size = 15
seed=random.randint(1, 1000)

for r in range(run):
    inicio = time.time()
    uda=udas[0]
    algo = pg.algorithm(uda)    
    
    algo.set_verbosity(1)
    algo.set_seed(seed)
    #print("inicializacao da populacao")
    #print(prob)
    pop = pg.population(prob,pop_size)
    #print("###########  ",pop, "  ################")
    results=[]
    for i in range(maxgen):
        pop = algo.evolve(pop)
        print(i,pop.champion_f, pop.champion_x)
        f,g = obj.fitness(pop.champion_x, flag=1)[0]
        l={
            'RUN':run, 'ITER':i, 'F':pop.champion_f[0], 'X':pop.champion_x,
            'ALG':algo.get_name().split(':')[0], 'SEED':seed,
            'MAX':g,
            'ALGNAME':algo.get_name().split(':')[1], 'MAXGEN':maxgen,
            }
        #print(l)
        results.append(l)
        
    fim = time.time()
    tempo = fim-inicio
    s_tempo = str(tempo)+'\n'

    with open(file_tempo, 'w') as f:
    	f.write(s_tempo)
    
    dataframe=pd.DataFrame(results)

    dataframe.to_pickle(path+basename + '_run_'+str(r) + '_' + os.uname()[1]+'__' +  
                time.strftime("%Y_%m_%d_") + time.strftime("_%Hh_%Mm_%S") +
                '.pkl') 
                






