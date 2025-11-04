from datetime import datetime, timezone
from typing import Union, List

from app.models import CharityProject, Donation


def invest_funds(
    target: Union[CharityProject, Donation],
    sources: List[Union[CharityProject, Donation]]
) -> List[Union[CharityProject, Donation]]:
    """Распределяет средства между проектами и пожертвованиями.

    Для нового проекта ищет незакрытые пожертвования
    и распределяет их средства.
    Для нового пожертвования ищет незакрытые проекты
    и распределяет средства в них.

    Args:
        target: Новый объект (проект или пожертвование) для инвестирования
        sources: Список незавершенных объектов для распределения средств

    Returns:
        List[Union[CharityProject, Donation]]: Список измененных объектов
    """
    current_time = datetime.now(timezone.utc)
    modified_objects = []
    for source in sources:
        if target.fully_invested:
            break
        target_invested = target.invested_amount or 0
        source_invested = source.invested_amount or 0
        required = target.full_amount - target_invested
        available = source.full_amount - source_invested
        amount = min(required, available)
        target.invested_amount = target_invested + amount
        source.invested_amount = source_invested + amount
        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = current_time
        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = current_time
        modified_objects.append(source)
    modified_objects.append(target)
    return modified_objects
