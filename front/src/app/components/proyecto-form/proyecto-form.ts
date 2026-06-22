import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Proyecto, ProyectoCreate, ProyectoUpdate } from '../../models/proyecto.model';

@Component({
  selector: 'app-proyecto-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './proyecto-form.html',
  styleUrl: './proyecto-form.css',
})
export class ProyectoForm {
  @Input() proyecto?: Proyecto;
  @Output() guardar = new EventEmitter<ProyectoCreate | ProyectoUpdate>();
  @Output() cancelar = new EventEmitter<void>();

  get editando(): boolean {
    return !!this.proyecto;
  }

  onSubmit(form: any): void {
    if (form.invalid) return;
    const data: ProyectoCreate | ProyectoUpdate = this.editando
      ? {
          nombre: form.value.nombre,
          descripcion: form.value.descripcion || null,
          fecha_inicio: form.value.fecha_inicio,
          fecha_fin: form.value.fecha_fin,
        }
      : {
          nombre: form.value.nombre,
          descripcion: form.value.descripcion || null,
          fecha_inicio: form.value.fecha_inicio,
          fecha_fin: form.value.fecha_fin,
        };
    this.guardar.emit(data);
  }
}
