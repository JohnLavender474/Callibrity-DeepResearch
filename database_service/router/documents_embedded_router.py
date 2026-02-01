from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from model.documents_embedded import (
    DocumentsEmbeddedCreate,
    DocumentsEmbeddedResponse,
)
from service import documents_embedded_service
from dependencies import get_db
import logging


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/database",
    tags=["database"],
)


@router.post("/documents-embedded")
def create_documents_embedded(
    document: DocumentsEmbeddedCreate,
    db: Session = Depends(get_db),
) -> DocumentsEmbeddedResponse:
    logger.info(f"Creating documents embedded entry: {document.filename}")

    created = documents_embedded_service.create_documents_embedded(
        db=db,
        document=document,
    )

    return created


@router.put("/documents-embedded")
def update_documents_embedded(
    document: DocumentsEmbeddedCreate,
    db: Session = Depends(get_db),
) -> DocumentsEmbeddedResponse:
    logger.info(f"Updating documents embedded entry: {document.filename}")

    updated = documents_embedded_service.update_documents_embedded(
        db=db,
        filename=document.filename,
        points=document.points,
    )

    return updated


@router.delete("/documents-embedded/{filename}")
def delete_documents_embedded(
    filename: str,
    db: Session = Depends(get_db),
):
    logger.info(f"Deleting documents embedded entry: {filename}")

    success = documents_embedded_service.delete_documents_embedded(
        db=db,
        filename=filename,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{filename}' not found",
        )

    return {"status": "ok", "filename": filename}


@router.get("/documents-embedded/{filename}")
def get_documents_embedded(
    filename: str,
    db: Session = Depends(get_db),
) -> DocumentsEmbeddedResponse:
    logger.info(f"Getting documents embedded entry: {filename}")

    document = documents_embedded_service.get_documents_embedded(
        db=db,
        filename=filename,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document '{filename}' not found",
        )

    return document
