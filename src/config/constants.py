"""
Constantes globales
"""

class HTTPStatus:
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    TOO_MANY_REQUESTS = 429
    INTERNAL_ERROR = 500

class ErrorMessages:
    CITY_NOT_FOUND = "Ville non trouvee"
    INVALID_API_KEY = "Cle API invalide"
    RATE_LIMIT_EXCEEDED = "Trop de requetes"
    NETWORK_ERROR = "Erreur reseau"
    TIMEOUT = "La requete a expired"