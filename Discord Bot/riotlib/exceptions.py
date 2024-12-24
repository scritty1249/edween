"""
# Riot Library - Exceptions
Houses Exceptions that may occur while interaction with the Riot API.
This library is intended to work with API's from Riot as of 12/23/2024
"""

class ApiException(Exception):
    def __init__(self, message: str):
        """Generic Exception class to raise when something fails while contacting the Riot API."""
        super().__init__(message)

class RateLimitExceededException(ApiException):
    def __init__(self, message: str = "API key rate limit exceeded."):
        """Exception class to raise when a Riot API key has exceeded it's rate limit when making a request.
            See [this link](https://developer.riotgames.com/docs/portal#web-apis_api-keys) for more details.
        """
        super().__init__(message)

class NotFoundException(ApiException):
    def __init__(self, message: str = "The requested information was not found."):
        """Exception class to raise when information does not exist. Intended to be used when requests to the Riot API returns a "Not Found" status."""
        super().__init__(message)

class BadKeyException(ApiException):
    def __init__(self, message: str = "Invalid Riot API key."):
        """Exception class to raise when a Riot API request is refused because of an invalid API key."""
        super().__init__(message)

class ServerErrorException(ApiException):
    def __init__(self, message: str = "An error occured after contacting the server."):
        """Exception class to raise when a Riot API responds with an Internal Server Error, Bad Gateway, Service Unavailable, or Gateway Timeout status."""
        super().__init__(message)