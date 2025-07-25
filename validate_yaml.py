import sys
import yaml
from typing import List, Dict, Union
from pydantic import BaseModel, Field, validator
from datetime import datetime


# Sub-models
class FhrConfig(BaseModel):
    start: int
    end: int
    step: int

class T0Config(BaseModel):
    start: str
    end: str
    freq: str

    @validator('start', 'end')
    def datetime_format(cls, v):
        # Just check it's a valid format like 2017-01-01T00
        try:
            datetime.strptime(v, "%Y-%m-%dT%H")
        except ValueError:
            raise ValueError(f"Invalid datetime format: {v}")
        return v

class SourceConfig(BaseModel):
    name: str
    t0: T0Config
    fhr: FhrConfig
    variables: List[str]
    levels: List[int]
    slices: Dict[str, Dict[str, List[float]]]

class TransformConfig(BaseModel):
    target_grid_path: str
    regridder_kwargs: Dict[str, Union[str, bool]]

class Transforms(BaseModel):
    horizontal_regrid: TransformConfig

class TargetConfig(BaseModel):
    name: str
    rename: Dict[str, str]
    chunks: Dict[str, int]

class ConfigModel(BaseModel):
    mover: Dict[str, Union[str, int]]
    directories: Dict[str, str]
    source: SourceConfig
    transforms: Transforms
    target: TargetConfig
    attrs: Dict[str, str]

def main(filepath):
    with open(filepath) as f:
        data = yaml.safe_load(f)
    try:
        ConfigModel(**data)
        print("YAML is valid.")
    except Exception as e:
        print("YAML validation failed:")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_yaml.py <file.yaml>")
        sys.exit(1)
    main(sys.argv[1])
