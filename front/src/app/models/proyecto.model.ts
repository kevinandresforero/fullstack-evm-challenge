export interface Proyecto {
  id: number;
  nombre: string;
  descripcion?: string;
  fecha_inicio: string;
  fecha_fin: string;
  fecha_modificacion: string;
  estado: string;
}

export interface ProyectoCreate {
  nombre: string;
  descripcion?: string;
  fecha_inicio: string;
  fecha_fin: string;
}

export interface ProyectoUpdate {
  nombre?: string;
  descripcion?: string;
  fecha_inicio?: string;
  fecha_fin?: string;
}
