# LastFM Music Recommendation Sandbox

This project leverages the LastFM Music Recommendation dataset available at http://ocelma.net/MusicRecommendationDataset/lastfm-1K.html. It seeks to demonstrate the efficacy of a few open source Python data engineering libraries in constructing a somewhat non-trivial ETL pipeline.

## The Question

If we define a user ‘session’ to be composed of one or more songs played by that user, where each song is started within 20 minutes of the previous song’s start time, create a list of the top 10 songs played in the top 50 longest sessions by tracks count. Deliver this as a tab-delimited file with the top 10 song names as well as their associated artist and play count within those sessions. 

## Technologies Chosen

- Kedro
    - Great CLI for bootstrapping a new data engineering or data science project. Takes care of most of the boilerplate, promotes great development practices, enables significant flexibility in pipeline construction, comes with extras that enable useful visualization of pipelines, and supports pipeline conversion to a large number of common DAG deployment targets including Airflow, Argo, Prefect, etc. Also makes data lineage a first class feature.
- Pandas
    - Industry standard tool for efficiently manipulating tabular data in Python. Robust and deeply tested API, highly optimized performance via C and Cython operations, and low maintenance overhead due to the fact that the vast majority of data professionals are familiar.
- Dask
    - Implements majority of the core Pandas DataFrame API while parallelizing the data structure. Enables storing DataFrame on disk when too large to fit into memory or on a cluster for distributed compute. Lighter weight than other distributed computing frameworks like Spark so great tool for prototyping Medium-Data projects that may become big over time.

## Running the Project

- Install docker and docker-compose
- Clone this repo with `git clone `
- Enter the repo with `cd lastfm-recs-sandbox`
- Run the pipeline with `docker-compose up pipeline_runner`
    - This takes ~15 mins to complete with 4 cores and 8 GB memory allocated to Docker. Roughly 10 minutes is downloading the tarball containing the data from the remote hosting server.
    - This will produce