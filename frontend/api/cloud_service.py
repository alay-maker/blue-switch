import logging
from typing import Any, Dict

import pandas as pd
import requests

from utils.config import CLOUD_RUN_URL

logger = logging.getLogger(__name__)


def obtener_dia_base(nodo: str = "valencia") -> pd.DataFrame:
    """Carga el CSV real de 24h generado por la fábrica de IA."""
    ruta_csv = f"frontend/artefactos/dia_base_{nodo.lower()}.csv"
    try:
        df = pd.read_csv(ruta_csv)
        if "time" in df.columns:
            df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        return df
    except FileNotFoundError:
        logger.error("⚠️ No se encontró %s.", ruta_csv)
        return pd.DataFrame()


def simular_escenario_mpc(modificadores: Dict[str, float], nodo: str = "valencia") -> Dict[str, Any]:
    """Aplica modificadores al día base y dispara la simulación real a Cloud Run."""
    df_base = obtener_dia_base(nodo)
    if df_base.empty:
        return {"error": "Faltan los archivos de artefactos CSV. Ejecuta la fábrica de IA."}

    df_base = df_base.copy()
    df_base["ambient_temperature"] += modificadores.get("temp_offset", 0.0)
    df_base["energy_spot_price_eur"] += modificadores.get("precio_offset", 0.0)
    df_base["d_async_kw"] = df_base["it_load_kw"] * 0.20

    capacidad_pico = float(df_base["it_load_kw"].max())
    capacidad_max_kw = capacidad_pico * modificadores.get("limite_servidor_mult", 1.20)

    payload = {
        "nodo": nodo.upper(),
        "is_simulation": True,
        "alpha_fin": modificadores.get("alpha", 0.33),
        "beta_eco": modificadores.get("beta", 0.33),
        "gamma_h2o": modificadores.get("gamma", 0.34),
        "capacidad_max_kw": capacidad_max_kw,
        "telemetria": df_base.to_dict(orient="records"),
    }

    logger.info("🚀 Disparando simulación real a Cloud Run para %s...", nodo.upper())

    try:
        respuesta = requests.post(CLOUD_RUN_URL, json=payload, timeout=20.0)
        respuesta.raise_for_status()
        return respuesta.json()
    except requests.exceptions.RequestException as exc:
        logger.error("❌ Error de API: %s", exc)
        return {"error": f"Fallo de conexión con la API: {str(exc)}"}