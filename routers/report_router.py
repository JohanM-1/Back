from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from Database.queries.reportsFuntions import get_report_base,insert_report,all_reportes,update_report,delete_report
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
async def get_report_id(id:int):
    response = await get_report_base(id)
    if(response != None):
        return response
    else:
        raise HTTPException(status_code=404, detail=f"Id no encontrado: {id}")
    

@router.get("/Reporte/all", tags=["Reporte"])
async def all_reports():
    response = await all_reportes()
    return response


class report_part(BaseModel):
    titulo: str = Field(..., max_length=100, description="Report title")
    descripcion: str = Field(..., max_length=1000, description="Detailed description of the snake sighting, including location, appearance, and behavior.")
    
@router.patch("/Reporte/Actualizar", tags=["Reporte"])
async def update_report_id(id:int,report_part:report_part):
    id_verif = await get_report_id(id)
    if (id_verif!=None):
        response = await update_report(
        id,
        titulo=report_part.titulo,
        descripcion=report_part.descripcion
        )
        return response

@router.delete("/Reporte/Actualizar", tags=["Reporte"])
async def delete_report_id(id:int):
    id_verif = await get_report_id(id)
    if (id_verif!=None):
        reponse = await delete_report(id)
        return reponse