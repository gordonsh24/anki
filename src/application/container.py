"""Dependency injection container configuration."""

from dependency_injector import containers, providers
from ..infrastructure import AnkiConnectCardRepository, AnkiConnectQuery
from ..infrastructure.anki_connect import AnkiConnectClient, AnkiConnectService
from .services import AnkiTodayService
from .presentation import ConsolePresenter
from .use_cases import AnkiToday

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
    
    anki_service = providers.Singleton(
        AnkiConnectService,
        client=anki_client,
    )
    
    anki_query = providers.Singleton(
        AnkiConnectQuery,
        client=anki_client,
    )
    
    card_repository = providers.Singleton(
        AnkiConnectCardRepository,
        query=anki_query,
    )
    
    # Application services
    service = providers.Singleton(
        AnkiTodayService,
        repository=card_repository,
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