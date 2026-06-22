export interface EvmIndicators {
  bac: number;
  pv: number;
  ev: number;
  ac: number;
  cv: number;
  sv: number;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  vac: number | null;
  cpi_interpretacion: string;
  spi_interpretacion: string;
}

export interface ActividadEvm {
  actividad_id: number;
  actividad_nombre: string;
  indicadores: EvmIndicators;
}

export interface ProyectoEvm {
  proyecto_id: number;
  proyecto_nombre: string;
  total_actividades: number;
  presupuesto_total: number;
  indicadores: EvmIndicators;
  actividades: ActividadEvm[];
}
