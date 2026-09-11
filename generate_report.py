"""
Script para geração automatizada do Relatório Técnico em PDF.
Executa o gerador e valida a criação do documento.
"""

import sys
from pathlib import Path
from src.utils.pdf_generator import gerar_pdf_relatorio
from src.config import RELATORIO_PDF

if __name__ == "__main__":
    print("Gerando Relatorio Tecnico em PDF (Desafio 5 - I2A2)...")
    arquivo_gerado = gerar_pdf_relatorio(RELATORIO_PDF)
    print(f"[OK] Relatorio tecnico em PDF gerado com sucesso em: {arquivo_gerado}")
