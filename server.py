import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sfm import generate_dense_point_cloud, generate_texture, reconstruct

import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PathRequest(BaseModel):
    path: str


@app.post("/dense")
async def dense(body: PathRequest):
    try:
        result = generate_dense_point_cloud(body.path)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


@app.post("/texture")
async def texture(body: PathRequest):
    try:
        result = generate_texture(body.path)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


@app.post("/reconstruct")
async def reconstruction(body: PathRequest):
    try:
        print(body.path)

        print("Generating point cloud")
        result1 = generate_dense_point_cloud(body.path)
        print(result1)

        print("Reconstructing mesh and texture")
        result2 = generate_texture(body.path)
        print("Finished reconstructing mesh at " + result2)

        return result2
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
