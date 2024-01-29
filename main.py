import os
import nbformat
from typing import Literal, List
from nbconvert import PDFExporter
from traitlets.config import Config
from typeguard import typechecked


class IpynbDirNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NotIpynbFileError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


@typechecked
def convert_ipynb_to_pdf(file_path: str, save_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    c = Config()
    c.PDFExporter.preprocessors = ["nbconvert.preprocessors.ExtractOutputPreprocessor"]
    c.PDFExporter.pdf_engine = (
        "xelatex"  # You can change this to another LaTeX engine if needed
    )

    pdf_exporter = PDFExporter(config=c)

    body, _ = pdf_exporter.from_notebook_node(notebook)

    with open(save_path, "wb") as f:
        f.write(body)


@typechecked
def ipynb_name_to_pdf(filename: str) -> str:
    if filename.endswith(".ipynb"):
        name, _ = filename.split(".")
        return name + ".pdf"
    raise NotIpynbFileError(message="file must have `ipynb` extension")


if __name__ == "__main__":
    pdf_dir: Literal["converted_pdf"] = "converted_pdf"
    os.makedirs(pdf_dir, exist_ok=True)
    ipynb_dir: Literal["ipynb_to_convert"] = "ipynb_to_convert"
    if not os.path.exists(ipynb_dir):
        raise IpynbDirNotFoundError(
            message="create `ipynb_to_convert` and put .ipynb files there"
        )
    files_to_convert: List[str] = os.listdir(ipynb_dir)
    for ipynb_file in files_to_convert:
        from_path: str = os.path.join(ipynb_dir, ipynb_file)
        to_path: str = os.path.join(pdf_dir, ipynb_name_to_pdf(ipynb_file))
        try:
            convert_ipynb_to_pdf(from_path, to_path)
        except ValueError:
            pass
