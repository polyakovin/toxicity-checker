---
updated: 2026-05-07
---
# Tech Stack
## Languages
| Language | Version | Detected | Notes |
|---|---|---|---|
| Python | 3.12 | package.json absent, assumed | Telegram bot |

## Frameworks
| Framework | Version | Purpose | Notes |
|---|---|---|---|
| aiogram | 3.x | Telegram Bot API framework | Async, modern |
| rapidfuzz | latest | Fuzzy string matching | Ingredient name matching |

## Tools
| Tool | Purpose | Notes |
|---|---|---|
| Tesseract | OCR for ingredient photos | Russian traineddata needed |
| pytesseract | Python binding for Tesseract | — |
| SQLite | Local database | aiosqlite for async |
| Docker | Containerization | Docker Compose for deployment |
| PubChem REST API | Chemical substance data | External lookup |
| OpenFoodFacts API | Product data by barcode | External lookup |
