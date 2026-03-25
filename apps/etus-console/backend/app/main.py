from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .etus_reader import (
    DOCS_ROOT,
    get_artifact_detail,
    get_feature_detail,
    get_memory,
    get_project_detail,
    get_validation,
    list_project_artifacts,
    list_projects,
)


app = FastAPI(title="ETUS Console API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "version": "0.1.0",
        "docs_root": str(DOCS_ROOT),
    }


@app.get("/api/projects")
def projects():
    return list_projects()


@app.get("/api/projects/{project_slug}")
def project_detail(project_slug: str):
    try:
        return get_project_detail(project_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/features")
def project_features(project_slug: str):
    try:
        return get_project_detail(project_slug).features
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/features/{feature_slug}")
def feature_detail(project_slug: str, feature_slug: str):
    try:
        return get_feature_detail(project_slug, feature_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/artifacts")
def project_artifacts(project_slug: str):
    try:
        return list_project_artifacts(project_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/artifacts/{artifact_key:path}")
def artifact_detail(project_slug: str, artifact_key: str):
    try:
        return get_artifact_detail(project_slug, artifact_key)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/validation")
def project_validation(project_slug: str):
    try:
        return get_validation(project_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/api/projects/{project_slug}/memory")
def project_memory(project_slug: str):
    try:
        return get_memory(project_slug)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
