#!/usr/bin/env python3

from src.application.container import Container

def main():
    # Create and configure the container
    container = Container()
    
    # Check if Anki is running and accessible
    version = container.anki_client().test_connection()
    if version is None:
        container.presenter().show_connection_error()
        return
    
    # Get the application instance and run it
    presenter = container.presenter()
    presenter.show_connection_success(version)
    
    anki = container.anki_today()
    anki.get_today_reviews()

if __name__ == "__main__":
    main() 