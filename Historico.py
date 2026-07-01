from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import RegistroPonto

router = APIRouter()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/historico", response_class=HTMLResponse)
def historico(
    request: Request,
    email: str,
    db: Session = Depends(get_db),
):

    hoje = datetime.now()
    ano_mes = hoje.strftime("%Y-%m")

    registros = (
        db.query(RegistroPonto)
        .filter(RegistroPonto.email == email, RegistroPonto.data.like(f"{ano_mes}%"))
        .order_by(RegistroPonto.data.asc(), RegistroPonto.hora.asc())
        .all()
    )

    registros_por_dia = {}

    for registro in registros:

        data = registro.data
        hora = registro.hora

        if data not in registros_por_dia:
            registros_por_dia[data] = []

        if len(registros_por_dia[data]) < 4:
            registros_por_dia[data].append(hora)

    historico = []

    for data, horarios in registros_por_dia.items():

        while len(horarios) < 4:
            horarios.append("--:--")

        historico.append(
            {
                "data": datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y"),
                "entrada1": horarios[0],
                "saida1": horarios[1],
                "entrada2": horarios[2],
                "saida2": horarios[3],
            }
        )

    return templates.TemplateResponse(
        "historico.html", {"request": request, "historico": historico}
    )
