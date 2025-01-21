"""Dependency injection container for the Anki Today application."""

from dependency_injector import containers, providers
from ..infrastructure import AnkiConnectCardRepository, AnkiConnectClient
from .presentation import ConsolePresenter
from .use_cases.today_review import AnkiToday


class Container(containers.DeclarativeContainer):
    """IoC container for dependency injection."""

    # Infrastructure
    anki_client = providers.Singleton(AnkiConnectClient)
    card_repository = providers.Singleton(AnkiConnectCardRepository, client=anki_client)

    # Presentation
    presenter = providers.Singleton(ConsolePresenter)

    # Use cases
    anki_today = providers.Singleton(
        AnkiToday,
        repository=card_repository,
        presenter=presenter
    ) 