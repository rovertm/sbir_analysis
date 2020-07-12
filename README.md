# sbir_analysis

### Table of Contents

1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [Results](#results)
5. [Licensing, Authors, and Acknowledgements](#licensing)

## Installation <a name="installation"></a>

* NLTK natural language processing package. Install instructions here: https://www.nltk.org/

Other: standard Python libraries across Anaconda distribution.

The code should run with no issues using Python versions 3.*.

## Project Motivation<a name="motivation"></a>

## Overview:

The objective of this notebook is to explore U.S. Government SBIR funding data through a top-down approach. Primary methods for analysis are natural language processing toolkits. 


## Part I: Building a Solicitations Dataframe

The exploration will begin with SBIR solicitations data for the past 3-years. Using API calls and dataframe concatenation, we will have a single-source dataframe for both open and closed solicitations to use in ongoing exploration.

## Part II: Tokenizing Keywords with NLTK -- NLP -- toolkits

The solicitation abstracts will be parsed and tokenized to review words by frequency, and by DoD branch thereafter.

## Part III: SBIR Awards Analysis

Awards data for the same three-year time period will be aggregated into a single dataframe and analyzed through collocation NLP methodologies -- Bi-grams analysis.

Following the Bi-gram results, the top Bi-gram frequencies assist in defining the 'groups' of the SBIR awards. 

The final product of awards analysis will be a bi-gram groups dataframe, which includes descriptive statistics referencing data from the companies (awardees) within each group.

## Part IV: NAICS Data -- Interfacing with the SAM awards API

While the SBIR solicitations and awards data is helpful for understanding bigger picture ideas and priorities, the companies themselves each have their own products and services even while in the same bi-gram grouping -- the industry NAICS codes will help us to see what it is that most of the awardees actually 'do' as registered businesses. The primary key to access and interface with this data is the DUNS number.

## Part V: Inception Analysis -- The Age of Awardee Companies

The final part of the analysis will case-study 'SWAP' and 'machine_learning' groups by looking at the inception dates of the associated awardees -- again, using the SAM API. 


## File Descriptions <a name="files"></a>

sbir_funding_overview.ipynb: Contains all code and visualizations.

source_data: dir containing .csv and .xlsx files

modules: dir containing all .py files for custom functions

## Results<a name="results"></a>

Please find the results summarized in the article [here](https://medium.com/@rovertkm/federal-sbir-funding-analysis-nlp-narrative-5eeed1f6a48e).

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

The source data for this project originated from the SBIR website: https://www.sbir.gov/
The initial export from the site - for this project - was done in July 2020.

All code is open for any and all usage.
