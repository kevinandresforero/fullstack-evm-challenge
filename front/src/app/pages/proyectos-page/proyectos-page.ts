import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ProyectoService } from '../../services/proyecto';
import { Proyecto } from '../../models/proyecto.model';
import { ProyectoForm } from '../../components/proyecto-form/proyecto-form';
import { ProyectoCreate, ProyectoUpdate } from '../../models/proyecto.model';

@Component({
  selector: 'app-proyectos-page',
  standalone: true,
  imports: [CommonModule, RouterModule, ProyectoForm],
  templateUrl: './proyectos-page.html',
  styleUrl: './proyectos-page.css',
})
export class ProyectosPage implements OnInit {
  proyectos: Proyecto[] = [];
  mostrarFormulario = false;
  proyectoEditando?: Proyecto;
  error = '';

  constructor(private proyectoService: ProyectoService) {}

  ngOnInit(): void {
    this.cargarProyectos();
  }

  cargarProyectos(): void {
    this.proyectoService.listar().subscribe({
      next: (data) => (this.proyectos = data),
      error: () => (this.error = 'Error al cargar proyectos'),
    });
  }

  abrirFormulario(): void {
    this.proyectoEditando = undefined;
    this.mostrarFormulario = true;
  }

  editar(proyecto: Proyecto): void {
    this.proyectoEditando = proyecto;
    this.mostrarFormulario = true;
  }

  onGuardar(data: ProyectoCreate | ProyectoUpdate): void {
    if (this.proyectoEditando) {
      this.proyectoService.actualizar(this.proyectoEditando.id, data as ProyectoUpdate).subscribe({
        next: () => { this.mostrarFormulario = false; this.cargarProyectos(); },
        error: () => (this.error = 'Error al actualizar proyecto'),
      });
    } else {
      this.proyectoService.crear(data as ProyectoCreate).subscribe({
        next: () => { this.mostrarFormulario = false; this.cargarProyectos(); },
        error: () => (this.error = 'Error al crear proyecto'),
      });
    }
  }

  onCancelar(): void {
    this.mostrarFormulario = false;
  }

  eliminar(id: number): void {
    if (confirm('¿Eliminar este proyecto?')) {
      this.proyectoService.eliminar(id).subscribe({
        next: () => this.cargarProyectos(),
        error: () => (this.error = 'Error al eliminar proyecto'),
      });
    }
  }
}
