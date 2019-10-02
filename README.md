# Using VIIRS nighttime satellite imagery to measure sub-national GDP and inequality on a global scale

Analysing socioeconomic development in an accurate and timely manner is critical for achieving the Sustainable Development Goals (SDGs) at both national and global levels. In past decades, scientists have proposed many methods for estimating human activity on Earth’s surface at various spatiotemporal scales using nighttime light (NTL) data. However, the NTL data and the associated processing methods have some characteristics that limit the reliability and applicability of using NTL for measuring socioeconomic development. In this study, we utilize the Isolation Forest machine learning algorithm for more intelligent data processing and the VIIRS NTL data to capture human activities. This model is highly flexible in that it can process the data in an unsupervised manner at various spatial scales. We have applied the method to measure and estimate the socioeconomic development on a global scale by estimating sub-national Gross domestic products (GDP). Results show that this method can produce reliable sub-national GDP data to estimate inequality. 

## Getting Started
In the data processing folder, all the data analysis codes used for this study are prepared using Python. The population data conversion codes, including the conversion of population raster data into point data and the conversion of GDP data into raster data, were created and converted using ArcPy in ArcGIS pro 2.4. The outlier detection model (using iForest algorithm) was written based on scikit-learn v0.21.3 versions. Specific instructions are included as comments in python files. The validation data folder contains the aggregated sub-national NTL results for validation. All input data are obtained from open data sources available online. 

### Prerequisites

Please install the latest version of ArcGIS Pro (2.7), Scikit-learn (v0.21.3), and Python 3
```
Give examples
```

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
pip install -U scikit-learn
```

or

```
conda install scikit-learn
```

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This work was supported in part by the Microsoft AI for Earth grant.
