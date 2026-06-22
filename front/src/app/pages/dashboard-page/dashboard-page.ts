import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { ProyectoService } from '../../services/proyecto';
import { ProyectoEvm, ActividadEvm } from '../../models/evm-indicators.model';
import { EvmChart } from '../../components/evm-chart/evm-chart';
import { EvmStatusIndicator } from '../../components/evm-status-indicator/evm-status-indicator';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  imports: [CommonModule, RouterModule, EvmChart, EvmStatusIndicator],
  templateUrl: './dashboard-page.html',
  styleUrl: './dashboard-page.css',
})
export class DashboardPage implements OnInit {
  proyectoId: number = 0;
  evmData?: ProyectoEvm;
  actividadesEvm: ActividadEvm[] = [];
  error = '';

  constructor(
    private route: ActivatedRoute,
    private proyectoService: ProyectoService,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      this.proyectoId = Number(params.get('id'));
      this.cargarEvm();
    });
  }

  cargarEvm(): void {
    this.proyectoService.obtenerEvm(this.proyectoId).subscribe({
      next: (data) => {
        this.evmData = data;
        this.actividadesEvm = data.actividades;
      },
      error: () => (this.error = 'Error al cargar indicadores EVM'),
    });
  }
}
