from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate, TicketPriority


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post(
    "/",
    response_model=TicketResponse,
    summary="Criar chamado",
    description=(
        "Cria um novo chamado vinculado automaticamente ao usuário autenticado. "
        "A categoria informada deve existir e o chamado é criado inicialmente "
        "com status OPEN."
    ),
)
def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    category = db.get(Category, ticket_data.category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada",
        )

    ticket = Ticket(
        title=ticket_data.title,
        description=ticket_data.description,
        status=TicketStatus.OPEN.value,
        priority=ticket_data.priority.value,
        requester_id=current_user.id,
        category_id=ticket_data.category_id,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Consultar chamado",
    description=(
        "Retorna os dados de um chamado específico. "
        "Usuários com perfil USER podem visualizar apenas seus próprios chamados. "
        "SUPPORT e ADMIN podem consultar qualquer chamado."
    ),
)
def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chamado não encontrado",
        )

    if current_user.role == "USER" and ticket.requester_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este chamado",
        )

    return ticket


@router.patch(
    "/{ticket_id}",
    response_model=TicketResponse,
    summary="Atualizar chamado",
    description=(
        "Atualiza os dados de um chamado existente. "
        "Usuários USER podem alterar apenas seus próprios chamados. "
        "SUPPORT e ADMIN podem atualizar qualquer chamado."
    ),
)
def update_ticket(
    ticket_id: int,
    ticket_data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    ticket = db.get(Ticket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chamado não encontrado",
        )

    if current_user.role == "USER" and ticket.requester_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar este chamado",
        )

    update_data = ticket_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        category = db.get(Category, update_data["category_id"])

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada",
            )

    for field, value in update_data.items():
        if field == "status":
            value = value.value

        if field == "priority":
            value = value.value

        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)

    return ticket


@router.get(
    "/",
    response_model=list[TicketResponse],
    summary="Listar chamados",
    description=(
        "Lista os chamados disponíveis para o usuário autenticado. "
        "Usuários USER visualizam apenas seus próprios chamados. "
        "SUPPORT e ADMIN visualizam todos. "
        "É possível filtrar por status, prioridade e categoria, "
        "além de utilizar paginação com skip e limit."
    ),
)
def list_tickets(
    status_filter: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    category_id: int | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = select(Ticket).order_by(Ticket.id.desc())

    if current_user.role == "USER":
        query = query.where(Ticket.requester_id == current_user.id)

    if category_id is not None:
        query = query.where(Ticket.category_id == category_id)

    if status_filter is not None:
        query = query.where(Ticket.status == status_filter.value)

    if priority is not None:
        query = query.where(Ticket.priority == priority.value)

    query = query.offset(skip).limit(limit)

    tickets = db.scalars(query).all()

    return tickets