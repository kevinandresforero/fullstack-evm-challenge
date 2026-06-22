import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Actividad, ActividadCreate, ActividadUpdate } from '../../models/actividad.model';

@Component({
  selector: 'app-actividad-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './actividad-form.html',
  styleUrl: './actividad-form.css',
})
export class ActividadForm {
  @Input() actividad?: Actividad;
  @Output() guardar = new EventEmitter<ActividadCreate | ActividadUpdate>();
  @Output() cancelar = new EventEmitter<void>();

  get editando(): boolean {
    return !!this.actividad;
  }

  onSubmit(form: any): void {
    if (form.invalid) return;
    const data: ActividadCreate | ActividadUpdate = {
      nombre: form.value.nombre,
      descripcion: form.value.descripcion || null,
      presupuesto: Number(form.value.presupuesto),
      porcentaje_avance_planificado: Number(form.value.porcentaje_avance_planificado),
      porcentaje_avance_real: Number(form.value.porcentaje_avance_real),
      costo_real: Number(form.value.costo_real),
      recursos: form.value.recursos || null,
      fecha_inicio: form.value.fecha_inicio || null,
      fecha_fin: form.value.fecha_fin || null,
    };
    this.guardar.emit(data);
  }
}
