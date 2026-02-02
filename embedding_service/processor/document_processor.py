import uuid
import logging

from typing import List

from pypdf import PdfReader
from qdrant_client.models import PointStruct

from service.embedding_service import EmbeddingService
from model.chunk_metadata import ChunkMetadata
from model.document_chunk import DocumentChunk


logger = logging.getLogger(__name__)


class DocumentProcessor:

    def __init__(self, embedding_service: EmbeddingService):
        logger.info("Initializing DocumentProcessor")
        self.embedding_service = embedding_service


    def _chunk_file(
        self,
        file_path: str,
        chunk_size: int
    ) -> List[DocumentChunk]:
        logger.debug(f"Extracting and chunking file: {file_path}")
        
        if file_path.endswith('.pdf'):
            logger.debug(f"Extracting text from PDF: {file_path}")
            reader = PdfReader(file_path)
            pages = []
            
            for page_num, page in enumerate(reader.pages, start=1):
                text = page.extract_text()
                pages.append(
                    DocumentChunk(
                        page_number=page_num,
                        text=text
                    )
                )
            
            total_chars = sum(len(chunk.text) for chunk in pages)
            logger.debug(
                f"Extracted {total_chars} characters from {len(pages)} pages"
            )
        elif file_path.endswith('.txt'):
            logger.debug(f"Extracting text from file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                logger.debug(
                    f"Extracted {len(text)} characters from text file"
                )
                pages = [
                    DocumentChunk(
                        page_number=1,
                        text=text
                    )
                ]
        else:
            logger.error(f"Unsupported file format for {file_path}")
            raise ValueError(
                f"Unsupported file format. Supported: .pdf, .txt"
            )
        
        logger.debug(
            f"Chunking {len(pages)} pages with chunk_size {chunk_size}"
        )
        chunks = []
        current_chunk_words = []
        current_size = 0
        current_page = None

        for page in pages:
            words = page.text.split()
            
            for word in words:
                word_size = len(word) + 1
                
                if (
                    current_size + word_size > chunk_size and
                    len(current_chunk_words) != 0
                ):
                    chunks.append(
                        DocumentChunk(
                            page_number=current_page,
                            text=" ".join(current_chunk_words)
                        )
                    )
                    current_chunk_words = [word]
                    current_size = word_size
                    current_page = page.page_number
                else:
                    if current_page is None:
                        current_page = page.page_number
                    current_chunk_words.append(word)
                    current_size += word_size

        if current_chunk_words:
            chunks.append(
                DocumentChunk(
                    page_number=current_page,
                    text=" ".join(current_chunk_words)
                )
            )

        logger.debug(f"Created {len(chunks)} chunks")
        return chunks


    def process_document(
        self,
        file_path: str,
        filename: str,
        chunk_size: int = 2000,
        custom_metadata: dict[str, any] = {}
    ) -> List[PointStruct]:
        logger.info(f"Processing document: {filename}")
        
        chunks = self._chunk_file(
            file_path=file_path,
            chunk_size=chunk_size
        )
        logger.info(
            f"Document '{filename}' split into {len(chunks)} chunks"
        )

        points = []
        for i, chunk in enumerate(chunks):
            vector = self.embedding_service.get_encoding(chunk.text)

            point_id = str(uuid.uuid4())

            chunk_metadata = ChunkMetadata(
                chunk_index=i,
                source_name=filename,
                content=chunk.text,
                page_number=chunk.page_number,
                custom_metadata=custom_metadata
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=chunk_metadata.model_dump()
                )
            )

        logger.info(
            f"Document processing complete: {len(points)} points created"
        )
        return points
