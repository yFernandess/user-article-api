from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schema import ArticleSchema
from core.dependencies import get_session, get_current_user


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ArticleSchema)
async def post_article(
    article: ArticleSchema,
    logged_in_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)):
    
    new_article: ArticleModel = ArticleModel(
                                             title=article.title,
                                             description=article.description,
                                             font_url=article.font_url,
                                             user_id=logged_in_user.id)

    db.add(new_article)
    await db.commit()

    return new_article


@router.get('/', response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


@router.get('/{article_id}', response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_article_by_id(article_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if article:
            return article
        else:
            raise HTTPException(detail='Article not found.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{article_id}', response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_article(article_id: int,
                      article: ArticleSchema,
                      db: AsyncSession = Depends(get_session),
                      logged_in_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        result = await session.execute(query)
        article_update: ArticleModel = result.scalars().unique().one_or_none()

        if article_update:
            if article.title:
                article_update.title = article.title

            if article.description:
                article_update.description = article.description

            if article.font_url:
                article_update.font_url = article.font_url

            if logged_in_user.id != article_update.user_id:
                article_update.user_id = logged_in_user.id            

            await session.commit()

            return article_update
        else:
            raise HTTPException(detail='Article not found.',
                                status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_id: int,
                         db: AsyncSession = Depends(get_session),
                         logged_in_user: UserModel = Depends(get_current_user)):

    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == article_id)
        query_filter = query.filter(ArticleModel.user_id == logged_in_user.id)
        result = await session.execute(query_filter)
        article_del: ArticleModel = result.scalars().unique().one_or_none()

        if article_del:
            await session.delete(article_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Article not found.',
                                status_code=status.HTTP_404_NOT_FOUND)