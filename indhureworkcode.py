# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 04:38:53 2023

@author: ACER
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.optimize import curve_fit
import seaborn as sns


def data_read(filename):
    """
    Reads data from a CSV file and returns cleaned dataframes with years and countries as columns.
    Parameters:
    filename (str): Name of the CSV file to read data from.
    Returns:
    df_years (pandas.DataFrame): Dataframe with years as columns and countries and indicators as rows.
    df_countries (pandas.DataFrame): Dataframe with countries as columns and years and indicators as rows.
    """
    # read the CSV file and skip the first 4 rows
    df = pd.read_csv(filename, skiprows=4)

    # drop unnecessary columns
    cols_to_drop = ['Country Code', 'Indicator Code', 'Unnamed: 66']
    df = df.drop(cols_to_drop, axis=1)

    # rename remaining columns
    df = df.rename(columns={'Country Name': 'Country'})

    # melt the dataframe to convert years to a single column
    df = df.melt(id_vars=['Country', 'Indicator Name'],
                 var_name='Year', value_name='Value')

    # convert year column to integer and value column to float
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')

    # separate dataframes with years and countries as columns
    df_years = df.pivot_table(
        index=['Country', 'Indicator Name'], columns='Year', values='Value')
    df_countries = df.pivot_table(
        index=['Year', 'Indicator Name'], columns='Country', values='Value')

    # clean the data
    df_years = df_years.dropna(how='all', axis=1)
    df_countries = df_countries.dropna(how='all', axis=1)

    return df_years, df_countries


def subset_data(df_years, countries, indicators):
    """
    Subsets the data to include only the selected countries, indicators, and years from 1990 to 2019.
    Returns the subsetted data as a new DataFrame.
    """
    years = list(range(1990, 2019))
    df = df_years.loc[(countries, indicators), years]
    df = df.transpose()
    return df


def map_corr(df, size=6):
    """Function creates heatmap of correlation matrix for each pair of 
    columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot (in inch)

    The function does not have a plt.show() at the end so that the user 
    can save the figure.
    """

    import matplotlib.pyplot as plt  # ensure pyplot imported

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    im = ax.matshow(corr, cmap='ocean')

    # setting ticks to column names
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=90)
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)

    # add colorbar
    cbar = fig.colorbar(im)

    # add title and adjust layout
    ax.set_title('Correlation Heatmap')
    plt.tight_layout()


def normalize_data(df):
    """
    Normalizes the data using StandardScaler.
    Parameters:
    df (pandas.DataFrame): Dataframe to be normalized.
    Returns:
    df_normalized (pandas.DataFrame): Normalized dataframe.
    """
    scaler = StandardScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    return df_normalized


def plot_normalized_data(df_normalized):
    """
    Plots a boxplot for each column in a normalized dataframe.
    Parameters:
    df_normalized (pandas.DataFrame): Normalized dataframe.
    """
    # Set custom style for plot
    sns.set_style('ticks')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax = sns.boxplot(data=df_normalized, orient='v', palette='Set3')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.set_title('Boxplot of Normalized Data')
    ax.set_ylabel('Value')

    # Add grid lines and remove top and right spines
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine(top=True, right=True)

    # Show plot
    plt.show()


def perform_kmeans_clustering(df, num_clusters):
    """
    Performs k-means clustering on the given dataframe.

    Args:
    data (pandas.DataFrame): Dataframe to be clustered.
    num_clusters (int): Number of clusters to form.

    Returns:
    cluster_labels (numpy.ndarray): Array of cluster labels for each data point.
    """
    # Create a KMeans instance with the specified number of clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)

    # Fit the model and predict the cluster labels for each data point
    cluster_labels = kmeans.fit_predict(df)

    return cluster_labels


def plot_clustered_data(df, cluster_labels, cluster_centers):
    """
    Plots the data points and cluster centers.

    Args:
    data (pandas.DataFrame): Dataframe containing the data points.
    cluster_labels (numpy.ndarray): Array of cluster labels for each data point.
    cluster_centers (numpy.ndarray): Array of cluster centers.
    """
    # Set the style of the plot
    plt.style.use('seaborn')

    # Create a scatter plot of the data points, colored by cluster label
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(df.iloc[:, 0], df.iloc[:, 1],
                         c=cluster_labels, cmap='summer')

    # Plot the cluster centers as black X's
    ax.scatter(cluster_centers[:, 0], cluster_centers[:,
               1], s=200, marker='X', c='black')

    # Set the x and y axis labels and title
    ax.set_xlabel(df.columns[0], fontsize=12)
    ax.set_ylabel(df.columns[1], fontsize=12)
    ax.set_title("K-Means Clustering Results", fontsize=14)

    # Add a grid and colorbar to the plot
    ax.grid(True)
    plt.colorbar(scatter)

    # Show the plot
    plt.show()


def filter_Methane_emission_data(filename, countries, indicators, start_year, end_year):
    """
    Reads a CSV file containing population data, filters it by countries and indicators, and returns a dataframe with
    years as columns and countries and indicators as rows.
    Parameters:
    filename (str): Path to the CSV file.
    countries (list): List of country names to filter by.
    indicators (list): List of indicator names to filter by.
    start_year (int): Starting year to select data from.
    end_year (int): Ending year to select data from.
    Returns:
    """
    # read the CSV file and skip the first 4 rows
    Methane_emission_data = pd.read_csv(filename, skiprows=4)

    # drop unnecessary columns
    cols_to_drop = ['Country Code', 'Indicator Code', 'Unnamed: 66']
    Methane_emission_data = Methane_emission_data.drop(cols_to_drop, axis=1)

    # rename remaining columns
    Methane_emission_data = Methane_emission_data.rename(
        columns={'Country Name': 'Country'})

    # filter data by selected countries and indicators
    Methane_emission_data = Methane_emission_data[Methane_emission_data['Country'].isin(countries) &
                                                  Methane_emission_data['Indicator Name'].isin(indicators)]

    # melt the dataframe to convert years to a single column
    Methane_emission_data = Methane_emission_data.melt(id_vars=['Country', 'Indicator Name'],
                                                       var_name='Year', value_name='Value')

    # convert year column to integer and value column to float
    Methane_emission_data['Year'] = pd.to_numeric(
        Methane_emission_data['Year'], errors='coerce')
    Methane_emission_data['Value'] = pd.to_numeric(
        Methane_emission_data['Value'], errors='coerce')

    # pivot the dataframe to create a single dataframe with years as columns and countries and indicators as rows
    Methane_emission_data = Methane_emission_data.pivot_table(index=['Country', 'Indicator Name'],
                                                              columns='Year', values='Value')

    # select specific years
    Methane_emission_data = Methane_emission_data.loc[:, start_year:end_year]

    return Methane_emission_data


def exp_growth(x, a, b):
    return a * np.exp(b * x)


def err_ranges(xdata, ydata, popt, pcov, alpha=0.05):
    n = len(ydata)
    m = len(popt)
    df = max(0, n - m)
    tval = -1 * stats.t.ppf(alpha / 2, df)
    residuals = ydata - exp_growth(xdata, *popt)
    stdev = np.sqrt(np.sum(residuals**2) / df)
    ci = tval * stdev * np.sqrt(np.diag(pcov))
    return ci

def predict_future(Methane_emission_data, countries, indicators, start_year, end_year):
    # select data for the given countries, indicators, and years
    data = filter_Methane_emission_data(Methane_emission_data, countries,
                                        indicators, start_year, end_year)

    # calculate the growth rate for each country and year
    growth_rate = np.zeros(data.shape)
    for i in range(data.shape[0]):
        popt, pcov = curve_fit(
            exp_growth, np.arange(data.shape[1]), data.iloc[i])
        ci = err_ranges(np.arange(data.shape[1]), data.iloc[i], popt, pcov)
        growth_rate[i] = popt[1]

    # plot the growth rate for each country
    fig, ax = plt.subplots()
    for i in range(data.shape[0]):
        ax.plot(np.arange(data.shape[1]), data.iloc[i],
                label=data.index.get_level_values('Country')[i])
    ax.set_xlabel('Year')
    ax.set_ylabel('Indicator Value')
    ax.set_title(', '.join(indicators))
    ax.legend(loc='best')
    plt.show()

    return growth_rate


if __name__ == '__main__':
    # Read the data
    csv_file = r"C:\Users\ACER\Downloads\worldbank.csv"
    df_years, df_countries = data_read(csv_file)

    # subset the data for the indicators of interest and the selected countries
    indicators = [
        'Methane emissions (kt of CO2 equivalent)', 'CO2 emissions (kt)']
    countries = ['India', 'United States', 'China', 'Japan']
    df = subset_data(df_years, countries, indicators)

    # normalize the data
    df_normalized = normalize_data(df)

    # perform clustering
    n_clusters = 3
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(df_normalized)
    cluster_centers = kmeans.cluster_centers_
     
print("Clustering Results points cluster_centers")
print(cluster_centers)
# plot the results
plot_clustered_data(df_normalized, cluster_labels, cluster_centers)

# predict future growth rates
growth_rates = predict_future(csv_file, ['India', 'China', 'United States'], ['Methane emissions (kt of CO2 equivalent)'], 1990, 2019)
print("Data fitting function Growth Rates")
print(growth_rates)

# plot correlation heatmap
map_corr(df, size=8)

# plot boxplot of normalized data
plot_normalized_data(df_normalized)