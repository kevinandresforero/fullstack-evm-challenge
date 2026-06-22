import { Routes } from '@angular/router';
import { ProyectosPage } from './pages/proyectos-page/proyectos-page';
import { ActividadesPage } from './pages/actividades-page/actividades-page';
import { DashboardPage } from './pages/dashboard-page/dashboard-page';

export const routes: Routes = [
  { path: '', redirectTo: '/proyectos', pathMatch: 'full' },
  { path: 'proyectos', component: ProyectosPage },
  { path: 'proyectos/:id/actividades', component: ActividadesPage },
  { path: 'dashboard/:id', component: DashboardPage },
];
