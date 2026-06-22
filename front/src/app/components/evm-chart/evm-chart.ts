import { Component, Input, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartType } from 'chart.js';
import { ActividadEvm } from '../../models/evm-indicators.model';

@Component({
  selector: 'app-evm-chart',
  standalone: true,
  imports: [BaseChartDirective],
  templateUrl: './evm-chart.html',
  styleUrl: './evm-chart.css',
})
export class EvmChart implements OnChanges {
  @Input() actividades: ActividadEvm[] = [];

  @ViewChild(BaseChartDirective) chart?: BaseChartDirective;

  chartType: ChartType = 'bar';

  chartData: ChartConfiguration['data'] = {
    labels: [],
    datasets: [
      { data: [], label: 'PV (Planificado)', backgroundColor: '#42a5f5' },
      { data: [], label: 'EV (Ganado)', backgroundColor: '#66bb6a' },
      { data: [], label: 'AC (Real)', backgroundColor: '#ef5350' },
    ],
  };

  chartOptions: ChartConfiguration['options'] = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['actividades']?.currentValue) {
      this.actualizarGrafico();
    }
  }

  private actualizarGrafico(): void {
    this.chartData.labels = this.actividades.map(a => a.actividad_nombre);
    this.chartData.datasets[0].data = this.actividades.map(a => a.indicadores.pv);
    this.chartData.datasets[1].data = this.actividades.map(a => a.indicadores.ev);
    this.chartData.datasets[2].data = this.actividades.map(a => a.indicadores.ac);
    this.chart?.update();
  }
}
