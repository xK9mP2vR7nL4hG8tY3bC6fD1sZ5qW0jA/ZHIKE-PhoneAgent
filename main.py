"""ZHIKE-PhoneAgent Backend API Server.

This module is kept for backward compatibility and development.
For production use, run: zhike-phoneagent (or uvx zhike-phoneagent)
"""

# Re-export app from the package
from zhike_phoneagent.server import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
