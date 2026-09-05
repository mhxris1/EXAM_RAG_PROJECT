import io
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
from docling.datamodel.base_models import DocumentStream
from database import save_image  # Database helper
from docling_core.types.doc import DoclingDocument

def parse_pdf_and_store_images(file_id: int, file_bytes: bytes, filename: str) -> DoclingDocument:
    """
    Parses a PDF using Docling:
    1. Extracts figure images and saves binary bytes directly to paper_images.
    2. Maps figure keys (fig_1.png) and captions.
    3. Returns Docling Doc
    """
    #Pipeline configuration
    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_picture_images = True  # Enable figure cropping
    
    #Rapid OCR for scanned docs
    pipeline_options.do_ocr = True
    pipeline_options.ocr_options = RapidOcrOptions()

    converter = DocumentConverter(
        format_options={"pdf": PdfFormatOption(pipeline_options=pipeline_options)}
    )

    #Convert binary file to readable stream
    #Fixed changed the name variable to name  and passed stream directily instead of through lambda
    doc_stream = DocumentStream(
        name=filename,
        #IO stream to feed the binary by using RAM preventing use of local storage 
        stream=io.BytesIO(file_bytes)
    )
    
    result = converter.convert(doc_stream)
    doc = result.document

    #Extract figure images, keys, and captions for SQLite insertion
    #Fixed error docling stores captions in list object so had to adjust for this
    for i, picture in enumerate(doc.pictures):
        image_key = f"fig_{i + 1}.png"
        
        # Safely extract caption from the captions list
        caption_text = f"Figure {i + 1}"
        if hasattr(picture, "captions") and picture.captions:
            extracted = [cap.text for cap in picture.captions if hasattr(cap, "text") and cap.text]
            if extracted:
                caption_text = " ".join(extracted)

        # Extract PIL Image object and save as raw binary bytes (PNG)
        if picture.image and picture.image.pil_image:
            img_byte_arr = io.BytesIO()
            picture.image.pil_image.save(img_byte_arr, format="PNG")
            image_bytes = img_byte_arr.getvalue()

            save_image(
                file_id=file_id,
                image_key=image_key,
                image_bytes=image_bytes,
                caption=caption_text
            )

    # 4. Return Markdown with embedded references (e.g., ![Caption](fig_1.png))
    return doc