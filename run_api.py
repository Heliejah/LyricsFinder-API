import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    logger.info("Starting Flask application...")
    from scripts.api import app
    
    if __name__ == "__main__":
        logger.info("Server starting at http://localhost:5000")
        # Changed from 0.0.0.0 to localhost for testing
        app.run(host='localhost', port=5000, debug=True)
        
except Exception as e:
    logger.error(f"Failed to start server: {str(e)}")
