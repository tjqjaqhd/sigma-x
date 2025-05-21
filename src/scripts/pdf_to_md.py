"""PDF 파일을 읽어 마크다운 파일로 저장하는 스크립트.

PyPDF2 라이브러리에 의존하며, PDF 내부 텍스트를 추출해 단순히 이어 붙인 후
지정한 마크다운 파일에 기록합니다. 환경에 따라 정확도가 달라질 수 있으므로
추출 후 내용을 검토해 수정하는 과정을 권장합니다.
"""

from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError as e:
    raise SystemExit(
        "PyPDF2가 설치되어 있지 않습니다. requirements.txt를 확인하세요"
    ) from e


def pdf_to_markdown(pdf_path: str, md_path: str) -> None:
    """주어진 PDF 파일을 읽어 텍스트를 추출 후 마크다운 파일로 저장."""
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    Path(md_path).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PDF를 마크다운으로 변환")
    parser.add_argument("pdf", help="원본 PDF 파일 경로")
    parser.add_argument("output", help="생성할 마크다운 파일 경로")
    args = parser.parse_args()

    pdf_to_markdown(args.pdf, args.output)
    print(f"완료: {args.output} 파일이 생성되었습니다.")
