<a href="https://www.du.edu/"><img src="https://www.du.edu/marcomm/assets/images/UniversityOfDenver-Signature.jpg" alt="University of Denver"></a>

# Global mapping of GDP at 1 km2 using VIIRS nighttime satellite imagery 

Frequent and rapid spatially explicit assessment of socioeconomic development is critical for achieving the Sustainable Development Goals (SDGs) at both national and global levels. In past decades, scientists have proposed many methods for estimating human activity on the Earth’s surface at various spatiotemporal scales using nighttime lights (NTL) data. NTL data and the associated processing methods have been limited their reliability and applicability for systematic measuring and mapping of socioeconomic development. This study utilizes Visible Infrared Imaging Radiometer Suite (VIIRS) NTL and the Isolation Forest machine learning algorithm for more intelligent data processing to capture human activities. We use machine learning and NTL data to map gross domestic product (GDP) at 1 km2. We then use these data products to derive inequality indexes (e.g. Gini coefficients) at nationally aggregate levels. This flexible approach processes the data in an unsupervised manner at various spatial scales. Our assessments show that this method produces accurate sub-national GDP data products for mapping and monitoring human development uniformly across the globe. 

## Getting Started
In the data processing folder, all the data analysis codes used for this study are prepared using Python. The population data conversion codes, including the conversion of population raster data into point data and the conversion of GDP data into raster data, were created and converted using ArcPy in ArcGIS pro 2.4. The outlier detection model (using iForest algorithm) was written based on scikit-learn v0.21.3 versions. Specific instructions are included as comments in python files. The validation data folder contains the aggregated sub-national NTL results for validation. All input data are obtained from open data sources available online. 

### Prerequisites

Please install the latest version Scikit-learn (v0.21.3)
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

The Isolation Forest algorithm is provided by Scikit learn. This read all the attributes of the point data The input variables are population and NTL intensity. This analysis will detect the outliers for countries in each of the income groups and change the outliers' NTL value to 0. 
```
python step_1_isolatedforest.py
```
### Data aggretation and Inequality indexes calculation

Data aggretation to construct Lorenz curve and produce GINI coefficients and 20:20 ratios based on cumulative subnational GDP distribution. GDP information is updated for each point so that they can be used to join with the original data points (based on pointid) and use point to raster tool in Arcgis Pro or Arcmap to create GDP at 1km2 across the globe in geotiff format. 

```
python step_2_aggregateData.py
```
## Authors

* **Xuantong Wang** - *University of Denver* - [Profile](https://scholar.google.com/citations?user=NsEDhRMAAAAJ&hl=en)

* **Dr.Paul Sutton** - *University of Denver* - [Profile](https://scholar.google.com/citations?user=cplEVLkAAAAJ&hl=en)

* **Bingxin Qi** - *University of Denver* 

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/tonyxuantong/NTL-GDP-VIIRS/blob/master/LICENSE) file for details

## Acknowledgments

* This work was supported in part by the Microsoft AI for Earth grant.
