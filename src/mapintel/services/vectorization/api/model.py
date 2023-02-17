import shutil
from typing import Any

import mlflow
from fastapi import APIRouter, File
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()


class Response(BaseModel):
    status: str


@router.post("/model", response_model=Response)
def model(file: bytes = File()):
    """Used to set model for vectorization.

    Args:
        File: Zipped file of model

    Returns:
        dict: status
    """
    with open("./src/mapintel/services/service1/model.zip", "wb") as f:
        f.write(file)
    shutil.unpack_archive(
        "./src/mapintel/services/service1/model.zip",
        "./src/mapintel/services/service1/model/",
        "zip",
    )
    return {"status": "Success"}


@router.get("/model")
def model(request: BaseModel):
    """Fetches model set for vectorization.

    Returns:
        File: Zipped file of model
    """
    return FileResponse("./src/mapintel/services/service1/model.zip")


class Request_vectors(BaseModel):
    docs: list[str]


class Response_vectors(BaseModel):
    status: str
    embeddings: Any

    class Config:
        arbitrary_types_allowed = True


@router.post("/vectors", response_model=Response_vectors)
def vectorisation(request: Request_vectors):
    """Vectorized docs.

    Args:
        List: List of strings/docs

    Returns:
        dict: Embeddings of docs
    """
    model = mlflow.pyfunc.load_model(model_uri="./src/mapintel/services/service1/model/")
    return {
        "status": "Success",
        "embeddings": model.predict(request.docs).tolist(),
    }  # np array not serialisable so must be turned to list


class Response_info(BaseModel):
    status: str
    metadata: dict


@router.get("/model/info", response_model=Response_info)
def vectorisation(request: BaseModel):
    """Info about model used for vectorization.

    Args:
        File: Zipped file of model

    Returns:
        dict: status
    """
    model = mlflow.pyfunc.load_model(model_uri="./src/mapintel/services/service1/model/")
    metadata = model.metadata.to_dict()
    return {"status": "Success", "metadata": metadata}  # np array not serialisable so must be turned to list