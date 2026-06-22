import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-evm-status-indicator',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './evm-status-indicator.html',
  styleUrl: './evm-status-indicator.css',
})
export class EvmStatusIndicator {
  @Input() label: string = '';
  @Input() value: number | null = null;
  @Input() interpretacion: string = '';

  get cssClass(): string {
    if (this.value === null) return 'indefinido';
    if (this.value > 1) return 'positivo';
    if (this.value < 1) return 'negativo';
    return 'neutro';
  }

  get icono(): string {
    if (this.value === null) return '—';
    if (this.value > 1) return '✓';
    if (this.value < 1) return '✗';
    return '•';
  }
}
