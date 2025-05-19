from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from pathlib import Path
from io import BytesIO
from src.usecases.invoices.save_template import SaveTemplateUseCase
from src.usecases.invoices.generate_pdf import GeneratePDFUseCase
from src.usecases.invoices.list_template import ListTemplateUseCase
from src.dependencies import (
    get_save_template_uc,
    get_list_template_uc,
    get_generate_pdf_uc,
)
from src.schemas.invoice_schema import InvoiceRequest


router = APIRouter(prefix="/api/v1/invoices", tags=["invoices"])
media_type = (
    "application/vnd" + ".openxmlformats-officedocument" + ".wordprocessingml.document"
)


@router.post("/templates/upload", status_code=201)
async def upload_docx(
    file: UploadFile = File(
        ...,
        media_type=media_type,
    ),
    uc: SaveTemplateUseCase = Depends(get_save_template_uc),
):
    data = await file.read()
    try:
        saved_path: Path = uc.execute(file.filename or "", data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse({"status": "success", "path": str(saved_path)})


@router.get("/templates")
async def list_templates(uc: ListTemplateUseCase = Depends(get_list_template_uc)):
    return list(uc.execute())


@router.post(
    "/generate",
    summary="Genera un PDF a partir de un template",
    description=(
        "Recibe un `.docx` válido (guardado desde Microsoft Word) "
        "y devuelve el PDF resultante. No se soportan `.odt` ni conversiones "
        "simples a `.docx`."
    ),
)
async def generate_pdf(
    req: InvoiceRequest,
    uc: GeneratePDFUseCase = Depends(get_generate_pdf_uc),
):

    try:
        invoice_entity = req.invoice.to_domain()
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))

    try:
        pdf_bytes = uc.execute(invoice_entity, req.template_name)
    except FileNotFoundError as e:

        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:

        raise HTTPException(
            status_code=503, detail=f"Error to generate PDF, check your template,{e}"
        )
    except Exception:

        raise HTTPException(status_code=500, detail="Error interno del servidor")

    filename = f"{invoice_entity.reference_code}.pdf"
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
