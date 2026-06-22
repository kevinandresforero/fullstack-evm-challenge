# EVM Project Manager — Frontend

Dashboard Angular para la gestión de proyectos con indicadores EVM.

## Requisitos previos

- Node.js 20+
- Angular CLI (`npm install -g @angular/cli`)

## Instalación

```bash
cd front
npm install --legacy-peer-deps
```

## Ejecución

```bash
npm start
# o
npx ng serve --proxy-config proxy.conf.json
```

Navegar a `http://localhost:4200`. El frontend espera el backend en `http://localhost:8000`.

## Build de producción

```bash
npx ng build
```

## Estructura

```
src/app/
├── models/          # Interfaces TypeScript
├── services/        # HTTP clients
├── components/      # Componentes reutilizables (form, chart, indicator)
├── pages/           # Páginas (smart components)
├── app.routes.ts    # Configuración de rutas
└── app.config.ts    # Providers (HTTP, Charts)
```

## Nota

Para desarrollo local con CORS, el backend FastAPI ya incluye `CORSMiddleware` configurado para permitir todos los orígenes.

La autenticación no está incluida en este demo. En producción, este frontend consumiría un API Gateway con autenticación WSO2/middleware.
