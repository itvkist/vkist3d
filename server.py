import os
import traceback

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sfm import generate_dense_point_cloud, generate_texture, reconstruct

import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR = os.path.join(BASE_DIR, 'projects')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectRequest(BaseModel):
    project_id: str


def resolve_project_path(project_id: str) -> str:
    """Resolve a project ID to its full path, rejecting any path traversal."""
    project_path = os.path.realpath(os.path.join(PROJECTS_DIR, project_id))
    if not project_path.startswith(os.path.realpath(PROJECTS_DIR)):
        raise HTTPException(status_code=400, detail="Invalid project ID")
    return project_path


@app.post("/dense")
async def dense(body: ProjectRequest):
    try:
        project_path = resolve_project_path(body.project_id)
        result = generate_dense_point_cloud(project_path)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


@app.post("/texture")
async def texture(body: ProjectRequest):
    try:
        project_path = resolve_project_path(body.project_id)
        result = generate_texture(project_path)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


@app.post("/reconstruct")
async def reconstruction(body: ProjectRequest):
    try:
        project_path = resolve_project_path(body.project_id)
        print(f"Starting reconstruction for project: {body.project_id}")

        print("Generating point cloud")
        result1 = generate_dense_point_cloud(project_path)
        print(result1)

        print("Reconstructing mesh and texture")
        result2 = generate_texture(project_path)
        print(f"Finished reconstruction for project: {body.project_id}")

        return {"projectId": body.project_id, "modelPath": result2}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail=traceback.format_exc())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
