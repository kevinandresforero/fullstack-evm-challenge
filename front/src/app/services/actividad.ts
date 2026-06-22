import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Actividad, ActividadCreate, ActividadUpdate } from '../models/actividad.model';
import { EvmIndicators } from '../models/evm-indicators.model';

@Injectable({ providedIn: 'root' })
export class ActividadService {
  private baseUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  private proyectoUrl(proyectoId: number): string {
    return `${this.baseUrl}/proyectos/${proyectoId}/actividades`;
  }

  listarPorProyecto(proyectoId: number): Observable<Actividad[]> {
    return this.http.get<Actividad[]>(this.proyectoUrl(proyectoId));
  }

  obtener(proyectoId: number, actividadId: number): Observable<Actividad> {
    return this.http.get<Actividad>(`${this.proyectoUrl(proyectoId)}/${actividadId}`);
  }

  crear(proyectoId: number, data: ActividadCreate): Observable<Actividad> {
    return this.http.post<Actividad>(this.proyectoUrl(proyectoId), data);
  }

  actualizar(proyectoId: number, actividadId: number, data: ActividadUpdate): Observable<Actividad> {
    return this.http.put<Actividad>(`${this.proyectoUrl(proyectoId)}/${actividadId}`, data);
  }

  eliminar(proyectoId: number, actividadId: number): Observable<Actividad> {
    return this.http.delete<Actividad>(`${this.proyectoUrl(proyectoId)}/${actividadId}`);
  }

  obtenerEvm(proyectoId: number, actividadId: number): Observable<EvmIndicators> {
    return this.http.get<EvmIndicators>(`${this.proyectoUrl(proyectoId)}/${actividadId}/evm`);
  }
}
