<a href="https://www.du.edu/"><img src="https://www.du.edu/marcomm/assets/images/UniversityOfDenver-Signature.jpg" alt="University of Denver"></a>

# Using VIIRS nighttime satellite imagery to measure sub-national GDP and inequality on a global scale

Analysing socioeconomic development in an accurate and timely manner is critical for achieving the Sustainable Development Goals (SDGs) at both national and global levels. In past decades, scientists have proposed many methods for estimating human activity on Earth’s surface at various spatiotemporal scales using nighttime light (NTL) data. However, the NTL data and the associated processing methods have some characteristics that limit the reliability and applicability of using NTL for measuring socioeconomic development. In this study, we utilize the Isolation Forest machine learning algorithm for more intelligent data processing and the VIIRS NTL data to capture human activities. This model is highly flexible in that it can process the data in an unsupervised manner at various spatial scales. We have applied the method to measure and estimate the socioeconomic development on a global scale by estimating sub-national Gross domestic products (GDP). Results show that this method can produce reliable sub-national GDP data to estimate inequality. 

## Getting Started
In the data processing folder, all the data analysis codes used for this study are prepared using Python. The population data conversion codes, including the conversion of population raster data into point data and the conversion of GDP data into raster data, were created and converted using ArcPy in ArcGIS pro 2.4. The outlier detection model (using iForest algorithm) was written based on scikit-learn v0.21.3 versions. Specific instructions are included as comments in python files. The validation data folder contains the aggregated sub-national NTL results for validation. All input data are obtained from open data sources available online. 

### Prerequisites

Please install the latest version of ArcGIS Pro (2.7), Scikit-learn (v0.21.3), and Python 3
```
pip install -U scikit-learn
```

or

```
conda install scikit-learn
```

## Running the analysis

The python scripts for data processsing are in the Python folder

### Run Isolation Forest to detect and reclassify outliers

The Isolation Forest algorithm is provided by Scikit learn. The input variables are population and NTL intensity. This analysis will detect the outliers for countries in each of the income groups and change the outliers' NTL value to 0. 
```
python step_1_isolatedforest.py
```
### Data aggretation and Inequality indexes calculation

Data aggretation to construct Lorenz curve and produce GINI coefficients and 20:20 ratios based on cumulative subnational GDP distribution.

Explain what these tests test and why

```
python step_2_aggregateData.py
```
## Authors

* **Xuantong Wang** - *University of Denver* - [Profile](https://scholar.google.com/citations?user=NsEDhRMAAAAJ&hl=en)

* **Dr.Paul Sutton** - *University of Denver* - [Profile](https://scholar.google.com/citations?user=cplEVLkAAAAJ&hl=en)

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/tonyxuantong/NTL-GDP-VIIRS/blob/master/LICENSE) file for details

## Acknowledgments

* This work was supported in part by the Microsoft AI for Earth grant.
