from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "/",
    response_model=CategoryResponse,
    summary="Criar categoria",
    description=(
        "Cria uma nova categoria de atendimento. "
        "Apenas usuários com perfil ADMIN podem realizar esta operação. "
        "O nome da categoria deve ser único."
    ),
)
def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar categorias",
        )

    existing_category = db.scalar(
        select(Category).where(Category.name == category_data.name)
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Categoria já cadastrada",
        )

    category = Category(
        name=category_data.name,
        description=category_data.description,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get(
    "/",
    response_model=list[CategoryResponse],
    summary="Listar categorias",
    description=(
        "Lista todas as categorias cadastradas no sistema, "
        "ordenadas alfabeticamente pelo nome. "
        "Qualquer usuário autenticado pode consultar esta lista."
    ),
)
def list_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    categories = db.scalars(
        select(Category).order_by(Category.name)
    ).all()

    return categories