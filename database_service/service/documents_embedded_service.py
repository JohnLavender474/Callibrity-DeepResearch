import uuid

from sqlalchemy.orm import Session

from model.documents_embedded import (
    DocumentsEmbeddedCreate,
    DocumentsEmbeddedResponse,
)
from model.documents_embedded_model import DocumentsEmbeddedModel


def create_documents_embedded(
    db: Session,
    document: DocumentsEmbeddedCreate,
) -> DocumentsEmbeddedResponse:
    db_document = DocumentsEmbeddedModel(
        id=str(uuid.uuid4()),
        filename=document.filename,
        points=document.points,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return DocumentsEmbeddedResponse(
        id=db_document.id,
        filename=db_document.filename,
        points=db_document.points,
    )


def update_documents_embedded(
    db: Session,
    filename: str,
    points: str,
) -> DocumentsEmbeddedResponse:
    db_document = db.query(DocumentsEmbeddedModel).filter(
        DocumentsEmbeddedModel.filename == filename
    ).first()

    if db_document is None:
        return create_documents_embedded(
            db=db,
            document=DocumentsEmbeddedCreate(
                filename=filename,
                points=points,
            ),
        )

    db_document.points = points
    db.commit()
    db.refresh(db_document)

    return DocumentsEmbeddedResponse(
        id=db_document.id,
        filename=db_document.filename,
        points=db_document.points,
    )


def delete_documents_embedded(
    db: Session,
    filename: str,
) -> bool:
    result = db.query(DocumentsEmbeddedModel).filter(
        DocumentsEmbeddedModel.filename == filename
    ).delete()

    db.commit()
    return result > 0


def get_documents_embedded(
    db: Session,
    filename: str,
) -> DocumentsEmbeddedResponse | None:
    db_document = db.query(DocumentsEmbeddedModel).filter(
        DocumentsEmbeddedModel.filename == filename
    ).first()

    if db_document is None:
        return None

    return DocumentsEmbeddedResponse(
        id=db_document.id,
        filename=db_document.filename,
        points=db_document.points,
    )
