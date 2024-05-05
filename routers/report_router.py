from __future__ import annotations
from fastapi import APIRouter
from Database.queries.reportsFuntions import get_report_base,insert_report,all_reportes
from .base_models.all_base_model import Reporte


router = APIRouter()

@router.post("/Reporte/create", tags=["Reporte"])
async def create_Georeference(Reporte_data: Reporte):
    response = await insert_report(
        titulo=Reporte_data.titulo,
        descripcion=Reporte_data.descripcion,
        comentario=Reporte_data.comentario,
        serpientes_id_serpientes=Reporte_data.serpientes_id_serpientes,
        usuario_id_usuario=Reporte_data.usuario_id_usuario,
        desarrollador_id_desarrollador=Reporte_data.desarrollador_id_desarrollador
    )

    return response

@router.get("/Reporte/id", tags=["Reporte"])
async def create_Georeference(id:int):
    response = await get_report_base(id)
    return response

@router.get("/Reporte/all", tags=["Reporte"])
async def all_reportes():
    response = await all_reportes()
    return response