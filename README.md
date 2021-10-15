# LastFM Music Recommendation Sandbox

This project leverages the LastFM Music Recommendation dataset available at http://ocelma.net/MusicRecommendationDataset/lastfm-1K.html. It seeks to demonstrate the efficacy of a few open source Python data engineering libraries in constructing a somewhat non-trivial ETL pipeline.

## The Question

If we define a user ‘session’ to be composed of one or more songs played by that user, where each song is started within 20 minutes of the previous song’s start time, create a list of the top 10 songs played in the top 50 longest sessions by tracks count. Deliver this as a tab-delimited file with the top 10 song names as well as their associated artist and play count within those sessions.

The result of this repo's attempt to answer this question can be produced via the steps below, but a copy is included for reference in the file `most_played_tracks.tsv`.

## Technologies Chosen

- Kedro
    - Great CLI for bootstrapping a new data engineering or data science project. Takes care of most of the boilerplate, promotes great development practices, enables significant flexibility in pipeline construction, comes with extras that enable useful visualization of pipelines, and supports pipeline conversion to a large number of common DAG deployment targets including Airflow, Argo, Prefect, etc. Also makes data lineage a first class feature.
- Pandas
    - Industry standard tool for efficiently manipulating tabular data in Python. Robust and deeply tested API, highly optimized performance via C and Cython operations, and low maintenance overhead due to the fact that the vast majority of data professionals are familiar.
- Dask
    - Implements majority of the core Pandas DataFrame API while parallelizing the data structure. Enables storing DataFrame on disk when too large to fit into memory or on a cluster for distributed compute. Lighter weight than other distributed computing frameworks like Spark so great tool for prototyping Medium-Data projects that may become big over time.

## Running the Project

- Install [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Clone this repo with `git clone https://github.com/blaizeberry4/lastfm-recs-sandbox`
- Enter the repo with `cd lastfm-recs-sandbox`
- Run the pipeline with `docker-compose up pipeline_runner`
    - This takes ~15-20 mins to complete with 4 cores and 8 GB memory allocated to Docker. Roughly 10 minutes is downloading the tarball containing the data from the remote hosting server.
    - Kedro will produce artifacts for every step in the pipeline in the `data` directory. The most played tracks for the longest sessions can be accessed at `data/04_deliverable/most_played_tracks.tsv`.
- Run the pipeline visualizer with `docker-compose up pipeline_visualizer`
    - This will provide a visualization component at `http://localhost:4141`

## Next Steps

- Add a robust [`pytest`](https://docs.pytest.org/en/6.2.x/) and [`hypothesis`](https://hypothesis.readthedocs.io/en/latest/) suite to prevent regressions catch unhandled edge cases.
- Install [`dask[distributed]`](https://distributed.dask.org/en/stable/) and configure a non-local cluster client to enable horizontal scaling. Subclass and override the [`KedroContext`](https://kedro.readthedocs.io/en/latest/kedro.framework.context.KedroContext.html) that injects the cluster client into the Kedro runtime.
- Use [`great-expectations`](https://greatexpectations.io/) for input and output data validation.
- Use [`kedro-airflow`](https://github.com/quantumblacklabs/kedro-airflow) or [a similar tool](https://kedro.readthedocs.io/en/stable/10_deployment/01_deployment_guide.html) to convert the pipeline to a DAG in another deployment framework to enable more sophisticated orchestration.