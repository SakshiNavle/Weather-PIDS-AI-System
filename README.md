# Weather-PIDS-AI-System

> **AI-powered weather-aware sensor calibration and monitoring platform for intelligent environmental risk detection, sensor sensitivity recommendations, and real-time alerts.**

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Frontend-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](#license)

---

## 📌 Overview

Weather conditions can significantly affect the reliability and operating behavior of environmental sensors. Changes in temperature, humidity, rainfall, wind speed, and severe weather conditions may require sensors to operate at different sensitivity levels.

The **Weather-PIDS-AI-System** is a software-based platform that combines:

- Live weather data
- Weather risk assessment
- Sensor management
- AI/ML-based calibration recommendations
- Automated weather alerts
- Historical weather monitoring
- Calibration recommendations
- Dashboard-based visualization

The system continuously connects environmental conditions with sensor calibration decisions, allowing users to understand **what is happening, why it matters, and what sensor action should be taken**.

---

# 🎯 Problem Statement

Environmental sensors operate under changing weather conditions. A fixed sensitivity configuration may not always be appropriate because:

- High humidity can affect sensor behavior.
- Heavy rainfall can influence environmental measurements.
- Strong winds can introduce measurement instability.
- Thunderstorms may create severe operating conditions.
- Different weather conditions may require different sensor sensitivity levels.

Traditional systems often monitor sensor values independently from environmental conditions.

This project addresses the problem by introducing a **weather-aware calibration decision system** that uses environmental conditions to generate actionable sensor recommendations.

---

# 💡 Proposed Solution

The system follows the pipeline:

```text
                 ┌─────────────────────┐
                 │   Weather Provider   │
                 │    OpenWeather API   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Weather Service   │
                 │ Fetch + Normalize   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Weather Risk      │
                 │      Engine         │
                 └──────────┬──────────┘
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
        ┌─────────────────┐   ┌─────────────────┐
        │ Alert Generation│   │ AI Calibration  │
        │                 │   │ Recommendation  │
        └────────┬────────┘   └────────┬────────┘
                 │                     │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │     Database        │
                 │ Weather / Alerts /  │
                 │ Recommendations /   │
                 │ Calibration History │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   FastAPI Backend   │
                 └──────────┬──────────┘
                            │ REST API
                            ▼
                 ┌─────────────────────┐
                 │ React + TypeScript  │
                 │     Dashboard       │
                 └─────────────────────┘
