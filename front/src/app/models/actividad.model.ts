export interface Actividad {
  id: number;
  proyecto_id: number;
  nombre: string;
  descripcion?: string;
  presupuesto: number;
  porcentaje_avance_planificado: number;
  porcentaje_avance_real: number;
  costo_real: number;
  recursos?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
  fecha_modificacion: string;
  estado: string;
}

export interface ActividadCreate {
  nombre: string;
  descripcion?: string;
  presupuesto: number;
  porcentaje_avance_planificado: number;
  porcentaje_avance_real: number;
  costo_real: number;
  recursos?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}

export interface ActividadUpdate {
  nombre?: string;
  descripcion?: string;
  presupuesto?: number;
  porcentaje_avance_planificado?: number;
  porcentaje_avance_real?: number;
  costo_real?: number;
  recursos?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}
