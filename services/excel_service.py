from openpyxl import Workbook
from pathlib import Path
import config
from models import Checklist
from extensions import db


def export_checklists_excel(path=None):
    wb = Workbook()
    ws = wb.active
    ws.title = 'Checklists'
    ws.append(['ID', 'Data', 'Técnico', 'Equipamento', 'Local', 'Status'])
    checks = Checklist.query.order_by(Checklist.data.desc()).all()
    for c in checks:
        ws.append([c.id, c.data.strftime('%Y-%m-%d %H:%M:%S'), c.tecnico, c.equipamento, c.local, c.status])
    dest = Path(path) if path else Path(config.EXCEL_FOLDER) / 'checklists.xlsx'
    dest.parent.mkdir(parents=True, exist_ok=True)
    wb.save(dest)
    return str(dest)
