#!/usr/bin/env python3
"""
Run script for the Old Age Home Management API
"""
import uvicorn
from decouple import config

if __name__ == "__main__":
    # Configuration from environment variables
    host = config("HOST", default="0.0.0.0")
    port = config("PORT", default=8000, cast=int)
    debug = config("DEBUG", default=True, cast=bool)
    
    # Run the application
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "warning"
    )
