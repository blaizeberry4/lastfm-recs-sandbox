from .extract import pipeline as extract_pipeline
from .eda import pipeline as eda_pipeline
from .transform import pipeline as transform_pipeline


pipeline = extract_pipeline + eda_pipeline + transform_pipeline