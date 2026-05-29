"""
Application principale Flask
Point d'entrée de l'API
"""

from flask import Flask, jsonify
from flask_cors import CORS
from src.api.routes.weather_routes import weather_bp
from src.api.middleware.error_handler import handle_errors
from src.config.settings import settings
from src.utils.logger import logger

def create_app():
    """Factory pattern pour créer l'application Flask"""
    
    # Créer l'app
    app = Flask(__name__)
    
    # Configuration
    app.config['DEBUG'] = settings.DEBUG
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    
    # CORS (pour permettre les requêtes depuis un frontend)
    CORS(app)
    
    # Enregistrer les blueprints (routes)
    app.register_blueprint(weather_bp)
    
    # Enregistrer les gestionnaires d'erreurs
    handle_errors(app)
    
    # Route de base pour tester
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "service": "Weather API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": [
                "/api/v1/weather/<city>",
                "/api/v1/weather/health",
                "/api/v1/weather/current?city=paris"
            ]
        }), 200
    
    # Route pour les métriques
    @app.route('/metrics', methods=['GET'])
    def get_metrics():
        from src.services.monitoring_service import monitoring
        return jsonify(monitoring.get_metrics()), 200
    
    logger.info(f"Application créée - Mode debug: {settings.DEBUG}")
    
    return app


# Point d'entrée pour lancer l'application
if __name__ == '__main__':
    app = create_app()
    
    # Lancer le serveur
    app.run(
        host='0.0.0.0',      # Écoute sur toutes les interfaces
        port=5000,            # Port par défaut
        debug=settings.DEBUG, # Mode debug si activé
        threaded=True         # Multi-thread
    )