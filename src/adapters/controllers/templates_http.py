from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from src.usecases.invoices.save_template import SaveTemplate
from src.dependencies import get_save_template_uc


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
    uc: SaveTemplate = Depends(get_save_template_uc),
):
    data = await file.read()
    try:
        saved_path: Path = uc.execute(file.filename or "", data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return JSONResponse({"status": "success", "path": str(saved_path)})


@router.get("/templates")
async def list_templates(uc: SaveTemplate = Depends(get_save_template_uc)):
    return list(uc.template_repository.list())
