from typing import Optional

from fastapi import APIRouter, Depends

from src.authentication.dependencies import get_current_user_authorizer
from src.app.database.database import get_repository
from src.articles.repository import ArticlesRepository
from src.authentication.models import User
from src.articles.dependencies import get_articles_filters
from src.articles.schemas import (
    ArticleForResponse,
    ArticlesFilters,
    ListOfArticlesInResponse,
)

router = APIRouter()

@router.get(
    "",
    response_model=ListOfArticlesInResponse,
    name="articles:list-articles",
)
async def list_articles(
    articles_filters: ArticlesFilters = Depends(get_articles_filters),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    articles_repo: ArticlesRepository = Depends(get_repository(ArticlesRepository)),
) -> ListOfArticlesInResponse:
    articles = await articles_repo.filter_articles(
        tag=articles_filters.tag,
        author=articles_filters.author,
        favorited=articles_filters.favorited,
        limit=articles_filters.limit,
        offset=articles_filters.offset,
        requested_user=user,
    )
    articles_for_response = [
        ArticleForResponse.from_orm(article) for article in articles
    ]
    return ListOfArticlesInResponse(
        articles=articles_for_response,
        articles_count=len(articles),
    )