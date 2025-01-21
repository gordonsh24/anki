"""IoC container for dependency injection."""

from dependency_injector import containers, providers

from src.infrastructure import AnkiConnectClient, AnkiConnectCardRepository, ConsolePresenter
from src.infrastructure.persistence.anki_connect.mapper import AnkiCardMapper
from src.application.use_cases.today_review import AnkiToday


class Container(containers.DeclarativeContainer):
    """IoC container for dependency injection."""

    # Infrastructure
    client = providers.Singleton(AnkiConnectClient)
    mapper = providers.Singleton(AnkiCardMapper)
    repository = providers.Singleton(
        AnkiConnectCardRepository,
        client=client,
        mapper=mapper
    )
    presenter = providers.Singleton(ConsolePresenter)

    # Use cases
    anki_today = providers.Singleton(
        AnkiToday,
        repository=repository,
        presenter=presenter
    ) 