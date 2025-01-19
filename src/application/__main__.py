"""Main entry point for the Anki Today application."""

from .container import Container

def main():
    """Run the application."""
    container = Container()
    
    # Test connection to Anki
    service = container.anki_service()
    version = service.test_connection()
    if version is None:
        print("Error: Could not connect to Anki. Please make sure Anki is running and AnkiConnect is installed.")
        return
    
    print(f"Connected to Anki (version {version})")
    
    # Execute the use case
    app = container.anki_today()
    app.execute()

if __name__ == "__main__":
    main() 