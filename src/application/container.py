"""Dependency injection container configuration."""

from dependency_injector import containers, providers
from ..infrastructure import AnkiConnectCardRepository, AnkiConnectClient
from .services import AnkiTodayService
from .presentation import ConsolePresenter


class Container(containers.DeclarativeContainer):
    """Application container."""

    # Infrastructure
    anki_client = providers.Singleton(AnkiConnectClient)
    card_repository = providers.Singleton(
        AnkiConnectCardRepository,
        client=anki_client
    )

    # Application
    anki_today_service = providers.Singleton(
        AnkiTodayService,
        card_repository=card_repository
    )
    console_presenter = providers.Singleton(ConsolePresenter) 