# NEX-DCP30 CMIP6 Watershed Visualization API

A FastAPI application for querying, processing, and visualizing NASA's NEX-DCP30 CMIP6 downscaled climate data at the watershed level.

## Features
- Watershed-level climate data aggregation (HUC4/HUC8/HUC12)
- NEX-DCP30 variable support (tasmax, tasmin, pr)
- Multi-model ensemble statistics
- Time-series and spatial data endpoints
- GeoJSON watershed boundary support

## Setup
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
