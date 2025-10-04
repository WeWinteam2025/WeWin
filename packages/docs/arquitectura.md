## Arquitectura (visión general)

```mermaid
flowchart LR
  U[Usuario] -->|HTTP| W[apps/web_html]
  W -->|HTMX fetch| Wp[Partials]
  W <--> |JSON REST| A[apps/api_django]
  A <--> |PostgreSQL| S[(Supabase)]

  subgraph Apps
    W
    A
    M[apps/mobile_flutter]
  end

  subgraph Packages
    D[packages/design]
    Doc[packages/docs]
  end

  W --> D
  M --> A
```

- apps/web_html: Landing, auth y dash con Vite + Tailwind + HTMX.
- apps/api_django: API REST (DRF), JWT, CORS, /healthz, DB en Supabase.
- packages/design: tokens de diseño compartidos (CSS variables + tokens Tailwind).
- packages/docs: documentación y diagramas.



