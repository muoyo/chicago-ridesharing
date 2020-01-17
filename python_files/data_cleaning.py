"""
##### DATA CLEANING #####

This module is for data cleaning.

"""

import pandas as pd
import numpy as np


dcmetro_FIPS = {
    'Alexandria City': 51510,
    'Arlington County': 51013,
    'Calvert County': 24009,
    'Charles County': 24017,
    'Clarke County': 51043,
    'Culpeper County': 51047,
    'District of Columbia': 11001,
    'Fairfax City': 51600,
    'Fairfax County': 51059,
    'Falls Church City': 51610,
    'Fauquier County': 51061,
    'Frederick County': 24021,
    'Fredericksburg City': 51630,
    'Jefferson County': 54037,
    'Loudoun County': 51107,
    'Manassas City': 51683,
    'Montgomery County': 24031,
    'Prince Georges County': 24033,
    'Prince William County': 51153,
    'Spotsylvania County': 51177,
    'Stafford County': 51179,
    'Warren County': 51187
}



def clean_homes_data(df_housing):
    """Clean up homes data"""
    
    # Filter down to the month we plan to use, June 2019
    df_housing_Jun2019 = df_housing[['RegionID', 'RegionName', 'State', 'Metro', 'SizeRank', '2019-06']]
    df_housing_Jun2019 = df_housing_Jun2019.rename(columns={'2019-06': 'MedianHousePrice'})
        
    df_dcmetro = df_housing_Jun2019.loc[df_housing_Jun2019['Metro'] == 'Washington-Arlington-Alexandria']
    df_dcmetro['FIPS'] = df_dcmetro['RegionName'].map(dcmetro_FIPS)
    
    return df_dcmetro

def merge_data(df_dcmetro, df_public_schools, df_private_schools, df_hospitals):
    """Merge homes data with public & private schools data"""
    
    public_schools_per_county = df_public_schools['COUNTYFIPS'].value_counts().to_frame()
    public_schools_per_county.reset_index(level=0, inplace=True)
    public_schools_per_county.rename(index=str, columns={"index": "FIPS", "COUNTYFIPS": "NumberOfPublicSchools"}, inplace=True)
    public_schools_per_county_dcmetro = public_schools_per_county.loc[public_schools_per_county['FIPS'].isin(dcmetro_FIPS.values())]
    
    private_schools_per_county = df_private_schools['COUNTYFIPS'].value_counts().to_frame()
    private_schools_per_county.reset_index(level=0, inplace=True)
    private_schools_per_county.rename(index=str, columns={"index": "FIPS", "COUNTYFIPS": "NumberOfPrivateSchools"}, inplace=True)
    private_schools_per_county_dcmetro = private_schools_per_county.loc[private_schools_per_county['FIPS'].isin(dcmetro_FIPS.values())]
    
    hospitals_per_county = df_hospitals['COUNTYFIPS'].value_counts().to_frame()
    hospitals_per_county.reset_index(level=0, inplace=True)
    hospitals_per_county.rename(index=str, columns={"index": "FIPS", "COUNTYFIPS": "NumberOfHospitals"}, inplace=True)
    hospitals_per_county['FIPS'] = pd.to_numeric(hospitals_per_county['FIPS'], errors='coerce')
    hospitals_per_county_dcmetro = hospitals_per_county.loc[hospitals_per_county['FIPS'].isin(dcmetro_FIPS.values())]
    
    df_dcmetro_merged = df_dcmetro.merge(public_schools_per_county_dcmetro, how='left', on='FIPS').merge(
                                        private_schools_per_county_dcmetro, how='left', on='FIPS').merge(
                                        hospitals_per_county_dcmetro, how='left', on='FIPS')
    
    df_dcmetro_merged['NumberOfSchools'] = df_dcmetro_merged['NumberOfPublicSchools'] + df_dcmetro_merged['NumberOfPrivateSchools']
    df_dcmetro_merged['PercentPublicSchools'] = df_dcmetro_merged['NumberOfPublicSchools'] / df_dcmetro_merged['NumberOfSchools']
    df_dcmetro_merged['PercentPrivateSchools'] = df_dcmetro_merged['NumberOfPrivateSchools'] / df_dcmetro_merged['NumberOfSchools']
    df_dcmetro_merged['NumberOfHospitals'] = df_dcmetro_merged['NumberOfHospitals'].fillna(0)
    
    return df_dcmetro_merged


def merge_population_data (df_dcmetro, df_population):
    """ Merge population data into dataset """
    
    df_population_dcarea = df_population.loc[df_population['State'].isin([' Virginia',' District of Columbia', ' Maryland',' West Virginia'])]
    df_population_dcarea.rename(columns = {'Geography_County':'RegionName'}, inplace = True)
    df_population_dcarea = df_population_dcarea.drop(['Id', 'Id2','State'], axis=1)
    
    df_dcmetro_merged = df_dcmetro.merge(df_population_dcarea, how='left', on='RegionName') 
    df_dcmetro_merged['PeoplePerSchool'] = df_dcmetro_merged['Population'] / df_dcmetro_merged['NumberOfSchools']
    df_dcmetro_merged['PeoplePerHospital'] = df_dcmetro_merged['Population'] / df_dcmetro_merged['NumberOfHospitals']
    df_dcmetro_merged['PeoplePerHospital'] = df_dcmetro_merged['PeoplePerHospital'].replace([np.inf, -np.inf], 0)
    df_dcmetro_merged['PublicSchoolsPerPerson'] =  df_dcmetro_merged['NumberOfPublicSchools'] / df_dcmetro_merged['Population']
    df_dcmetro_merged['PrivateSchoolsPerPerson'] =  df_dcmetro_merged['NumberOfPrivateSchools'] / df_dcmetro_merged['Population']
        
    return df_dcmetro_merged



def clean_data(df_housing, df_public_schools, df_private_schools, df_hospitals, df_population):
    """
    This is the one function called that will run all the support functions.
    
    :return: cleaned dataset to be passed to hypothesis testing and visualization modules.
    """
    
    df_dcmetro = clean_homes_data(df_housing)
    df_dcmetro = merge_data(df_dcmetro, df_public_schools, df_private_schools, df_hospitals)
    df_dcmetro = merge_population_data(df_dcmetro, df_population)
    
    
    return df_dcmetro