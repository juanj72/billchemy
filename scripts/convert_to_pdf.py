import argparse
import subprocess
import sys
from pathlib import Path


def convert_docx_to_pdf(
    input_path: Path, output_dir: Path, filter_name: str = "pdf:writer_pdf_Export"
) -> Path:
    """
    Convierte `input_path` (.docx) a PDF colocándolo dentro de `output_dir`.
    Usa LibreOffice headless con el filtro `filter_name`.
    Devuelve la ruta al PDF generado.
    """
    input_path = input_path.resolve()
    output_dir = output_dir.resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Archivo de entrada no encontrado: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Selecciona el comando disponible
    office_cmd = "soffice"  # normalmente está en PATH
    # Ejecuta la conversión
    cmd = [
        office_cmd,
        "--headless",
        "--convert-to",
        filter_name,
        "--outdir",
        str(output_dir),
        str(input_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Error en la conversión:\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    pdf_path = output_dir / f"{input_path.stem}.pdf"
    if not pdf_path.exists():
        existing = [p.name for p in output_dir.iterdir()]
        raise RuntimeError(
            f"No se generó el PDF. Busqué en {output_dir} y encontré: {existing}"
        )

    return pdf_path


def main():
    parser = argparse.ArgumentParser(
        description="Convierte un .docx a PDF usando LibreOffice headless."
    )
    parser.add_argument("input", type=Path, help="Ruta al archivo .docx de entrada")
    parser.add_argument(
        "output_dir", type=Path, help="Directorio donde se guardará el PDF"
    )
    args = parser.parse_args()

    try:
        pdf_file = convert_docx_to_pdf(args.input, args.output_dir)
        print(f"✅ PDF generado en: {pdf_file}")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
