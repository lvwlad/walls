from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import desc, select
from sqlalchemy.orm import Session
from database import get_db
from models.models import Post, User
from schemas.posts import AllPost, PostCreate, UsersPostsModel
from services.users import get_current_user_id

router = APIRouter(prefix="/api", tags=["posts"])


@router.post("/posts")
async def create_post(
    post: PostCreate,
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    serialized_blocks = [block.model_dump() for block in post.content_blocks]
    new_post = Post(content=serialized_blocks, owner=user_id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.get("/posts", response_model=list[AllPost])
async def get_main_post(
    limit: int | None = Query(default=None),
    offset: int | None = Query(default=None),
    session: Session = Depends(get_db),
):
    query = (
        select(User.name, Post.content, Post.created_at)
        .where(Post.owner == User.id)
        .order_by(desc(Post.created_at))
        .limit(limit)
        .offset(offset)
    )
    return session.execute(query)


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: int,
    session: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    post = session.query(Post).filter(Post.id == post_id, Post.owner == user_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": "Пост не найден"},
        )
    session.delete(post)
    session.commit()
    return {"message": f"Пост {post_id} удалён"}


@router.get("/users/{username}/posts", response_model=list[UsersPostsModel])
async def get_users_posts(
    username: str = Path(),
    limit: int | None = Query(default=None),
    offset: int | None = Query(default=None),
    session: Session = Depends(get_db),
):
    user = session.scalar(select(User).where(User.name == username))
    if not user:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": f"Пользователь {username} не найден"},
        )

    query = (
        select(Post)
        .where(Post.owner == user.id)
        .order_by(desc(Post.created_at))
        .limit(limit)
        .offset(offset)
    )
    return session.scalars(query)
