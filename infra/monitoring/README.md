Prometheus + Grafana

- Prometheus scrape config at infra/monitoring/prometheus/prometheus.yml
- Grafana provisioning files under infra/monitoring/grafana/provisioning
- Expose Grafana on port 3000

Configure the FastAPI app to expose Prometheus metrics at `/metrics` (use `prometheus_client` library).
