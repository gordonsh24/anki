from dependency_injector import containers, providers
from ..integration import AnkiConnectClient
from .services import Query, AnkiTodayService
from .presentation import ConsolePresenter
from .anki_today import AnkiToday

class Container(containers.DeclarativeContainer):
    """IoC container for dependency injection."""
    
    # Configuration
    config = providers.Configuration(default={
        "host": "localhost",
        "port": 8765,
    })
    
    # Infrastructure
    anki_client = providers.Singleton(
        AnkiConnectClient,
        host=config.host,
        port=config.port,
    )
    
    # Application services
    query = providers.Singleton(
        Query,
        client=anki_client,
    )
    
    service = providers.Singleton(
        AnkiTodayService,
        query=query,
    )
    
    # Presentation
    presenter = providers.Singleton(
        ConsolePresenter,
    )
    
    # Application
    anki_today = providers.Singleton(
        AnkiToday,
        service=service,
        presenter=presenter,
    ) 