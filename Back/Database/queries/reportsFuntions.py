from ast import List
import asyncio
from Database.models.DataBaseModel import async_session, Usuario, Reporte
from sqlalchemy import select

async def insert_reporte(reports: list[dict]) -> None:
    async with async_session() as session:
        try:
            for report_data in reports:
                report = Reporte(**report_data)
                session.add(report)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise


async def view_reportes():
    async with async_session() as session:
        # Realizar una consulta para obtener todos los reportes
        stmt = select(Reporte)
        result = await session.execute(stmt)
        reportes = result.scalars().all()

        # Imprimir los reportes
        for reporte in reportes:
            print(reporte+"1")