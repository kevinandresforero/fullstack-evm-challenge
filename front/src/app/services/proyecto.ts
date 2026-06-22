import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Proyecto, ProyectoCreate, ProyectoUpdate } from '../models/proyecto.model';
import { ProyectoEvm } from '../models/evm-indicators.model';

@Injectable({ providedIn: 'root' })
export class ProyectoService {
  private apiUrl = 'http://localhost:8000/api/proyectos';

  constructor(private http: HttpClient) {}

  listar(): Observable<Proyecto[]> {
    return this.http.get<Proyecto[]>(this.apiUrl);
  }

  obtener(id: number): Observable<Proyecto> {
    return this.http.get<Proyecto>(`${this.apiUrl}/${id}`);
  }

  crear(data: ProyectoCreate): Observable<Proyecto> {
    return this.http.post<Proyecto>(this.apiUrl, data);
  }

  actualizar(id: number, data: ProyectoUpdate): Observable<Proyecto> {
    return this.http.put<Proyecto>(`${this.apiUrl}/${id}`, data);
  }

  eliminar(id: number): Observable<Proyecto> {
    return this.http.delete<Proyecto>(`${this.apiUrl}/${id}`);
  }

  obtenerEvm(id: number): Observable<ProyectoEvm> {
    return this.http.get<ProyectoEvm>(`${this.apiUrl}/${id}/evm`);
  }
}
