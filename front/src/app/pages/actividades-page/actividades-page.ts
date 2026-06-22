import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ActividadService } from '../../services/actividad';
import { ProyectoService } from '../../services/proyecto';
import { Proyecto } from '../../models/proyecto.model';
import { ActividadForm } from '../../components/actividad-form/actividad-form';
import { Actividad, ActividadCreate, ActividadUpdate } from '../../models/actividad.model';

@Component({
  selector: 'app-actividades-page',
  standalone: true,
  imports: [CommonModule, RouterModule, ActividadForm],
  templateUrl: './actividades-page.html',
  styleUrl: './actividades-page.css',
})
export class ActividadesPage implements OnInit {
  proyectoId: number = 0;
  proyecto?: Proyecto;
  actividades: Actividad[] = [];
  mostrarFormulario = false;
  actividadEditando?: Actividad;

  constructor(
    private route: ActivatedRoute,
    private actividadService: ActividadService,
    private proyectoService: ProyectoService,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.proyectoId = Number(params.get('id'));
      this.cargarProyecto();
      this.cargarActividades();
    });
  }

  cargarProyecto(): void {
    this.proyectoService.obtener(this.proyectoId).subscribe({
      next: (data) => (this.proyecto = data),
    });
  }

  cargarActividades(): void {
    this.actividadService.listarPorProyecto(this.proyectoId).subscribe({
      next: (data) => (this.actividades = data),
    });
  }

  abrirFormulario(): void {
    this.actividadEditando = undefined;
    this.mostrarFormulario = true;
  }

  editar(actividad: Actividad): void {
    this.actividadEditando = actividad;
    this.mostrarFormulario = true;
  }

  onGuardar(data: ActividadCreate | ActividadUpdate): void {
    if (this.actividadEditando) {
      this.actividadService.actualizar(this.proyectoId, this.actividadEditando.id, data as ActividadUpdate).subscribe({
        next: () => { this.mostrarFormulario = false; this.cargarActividades(); },
      });
    } else {
      this.actividadService.crear(this.proyectoId, data as ActividadCreate).subscribe({
        next: () => { this.mostrarFormulario = false; this.cargarActividades(); },
      });
    }
  }

  onCancelar(): void {
    this.mostrarFormulario = false;
  }

  eliminar(id: number): void {
    if (confirm('¿Eliminar esta actividad?')) {
      this.actividadService.eliminar(this.proyectoId, id).subscribe({
        next: () => this.cargarActividades(),
      });
    }
  }
}
