"""
Script para empacotar todos os arquivos do projeto no formato ZIP para entrega do Desafio 5 (I2A2).
Gera o arquivo 'desafio5_entrega.zip' contendo todo o código-fonte, dados, testes e documentação.
"""

import os
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ZIP_OUTPUT = BASE_DIR / "desafio5_entrega.zip"

# Diretórios e arquivos a incluir
ITENS_INCLUIR = [
    "src",
    "tests",
    "app.py",
    "run_demo.py",
    "generate_report.py",
    "package_submission.py",
    "relatorio_tecnico.md",
    "relatorio_tecnico.pdf",
    "requirements.txt",
    "README.md",
    "LICENSE",
    ".env.example",
    ".gitignore"
]

EXTENSOES_IGNORAR = {".pyc", ".pyo", ".pyd", ".log", ".tmp"}
DIR_IGNORAR = {"__pycache__", ".pytest_cache", ".venv", "venv", ".git", ".idea", ".vscode"}


def empacotar_projeto():
    print("Iniciando empacotamento do projeto para entrega...")
    
    if ZIP_OUTPUT.exists():
        ZIP_OUTPUT.unlink()

    total_arquivos = 0
    with zipfile.ZipFile(ZIP_OUTPUT, "w", zipfile.ZIP_DEFLATED) as zipf:
        for item_nome in ITENS_INCLUIR:
            item_path = BASE_DIR / item_nome
            if not item_path.exists():
                print(f"[AVISO] Item '{item_nome}' nao encontrado. Ignorando...")
                continue

            if item_path.is_file():
                zipf.write(item_path, arcname=item_nome)
                total_arquivos += 1
                print(f"  + Arquivo: {item_nome}")
            elif item_path.is_dir():
                for root, dirs, files in os.walk(item_path):
                    # Filtra diretórios ignorados
                    dirs[:] = [d for d in dirs if d not in DIR_IGNORAR]
                    for file in files:
                        ext = Path(file).suffix
                        if ext in EXTENSOES_IGNORAR:
                            continue
                        full_path = Path(root) / file
                        arcname = full_path.relative_to(BASE_DIR)
                        zipf.write(full_path, arcname=str(arcname))
                        total_arquivos += 1
                        print(f"  + {arcname}")

    tamanho_mb = ZIP_OUTPUT.stat().st_size / (1024 * 1024)
    print("\n[OK] Empacotamento concluido com sucesso!")
    print(f"Arquivo gerado: {ZIP_OUTPUT.name} ({tamanho_mb:.2f} MB - {total_arquivos} arquivos)")


if __name__ == "__main__":
    empacotar_projeto()
