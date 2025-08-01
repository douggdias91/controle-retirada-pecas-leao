
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def gerar_pdf(nome, peca, obs, data):
    arquivo = f"requisicoes/{nome.replace(' ', '_')}_{peca.replace(' ', '_')}.pdf"
    os.makedirs("requisicoes", exist_ok=True)
    c = canvas.Canvas(arquivo, pagesize=A4)
    c.drawString(100, 800, f"Solicitante: {nome}")
    c.drawString(100, 780, f"Peça: {peca}")
    c.drawString(100, 760, f"Observações: {obs}")
    c.drawString(100, 740, f"Data/Hora: {data}")
    c.save()
    return arquivo
