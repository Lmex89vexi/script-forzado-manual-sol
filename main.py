import requests
from loguru import logger
from datetime import datetime
import os

from api_server_request import (
    api_server_get_request,
    api_server_delete_request,
    api_server_put_request,
)

# ===================== servicios APISOL-INTERNO =====================
APISOL_INTERNO = os.getenv("APISOL_INTERNO", "http://localhost:38495")
URL_QUERY_SOL_BY_DATE_FASE = "/v1/step-functions/solicitudes/fases/{}/termino/"
# ===================== servicios APISOL-INTERNO =====================

# ===================== servicios APISOL-ORQUESTADOR =====================
APISOL_ORQUESTADOR = os.getenv("APISOL_ORQUESTADOR", "http://localhost:46227")
URL_DELETE_WORKFLOW_SOLICITUD = "/v1/solicitud/{}/eliminar-solicitud-wf/{}/"  # id_sol, email
URL_FORZAR_TERMINO_SOLICITUD = "/v1/solicitud/{}/forzar-termino-solcitud-wf/{}/"  # id_sol, email
# ===================== servicios APISOL-INTERNO =====================

# ===================== PARAMS TO main ===============================
#DATE_START = "2023-07-20 00:00:00"
#DATE_END = "2023-07-21 23:59:59"
DATE_START = "2023-01-01 11:35:47"
DATE_END = "2023-12-12 11:35:47"
ID_FASE = 23
# ===================== PARAMS TO main ===============================

# ===================== CONSTANTES ===============================
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
# ===================== CONSTANTES ===============================


def main(date_start, date_end, id_fase: int):
    date_start = datetime.strptime(date_start, DATE_FORMAT)
    date_end = datetime.strptime(date_end, DATE_FORMAT)

    params = {"date_start": date_start, "date_end": date_end}

    logger.info(f"---fechas para iniciar  {locals()} ")
    solicitudes_en_proceso = api_server_get_request(
        url=APISOL_INTERNO + URL_QUERY_SOL_BY_DATE_FASE.format(id_fase), params=params
    )

    if not solicitudes_en_proceso:
        return

    logger.info(f"---Total de solicitudes a terminar {len(solicitudes_en_proceso)} --- ")

    for solicitud in solicitudes_en_proceso:
        id_solicitud = solicitud.get("id_solicitud")
        email = solicitud.get("email")

        if not id_solicitud or not email:
            continue

        try:
            response = api_server_delete_request(
                url=APISOL_ORQUESTADOR + URL_DELETE_WORKFLOW_SOLICITUD.format(id_solicitud, email)
            )
            logger.info(
                f" DELETE worflow sol--- id_solicitud {id_solicitud} email {email}  ----- response {response}"
            )
            response = api_server_put_request(
                url=APISOL_ORQUESTADOR + URL_FORZAR_TERMINO_SOLICITUD.format(id_solicitud, email), 
                data={}
            )
            logger.info(
                f" FORZAR-TERMINO --- id_solicitud {id_solicitud} email {email}  ----- response {response}"
            )
        except Exception as exc:
            logger.error(
                f" ---Error en mandar evento wh id_solicitud {id_solicitud}  email {email} Error:{exc}"
            )


if __name__ == "__main__":
    main(date_start=DATE_START, date_end=DATE_END, id_fase=ID_FASE)
