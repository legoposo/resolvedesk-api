from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.category import Category
from app.models.ticket import Ticket, TicketStatus
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.post("/", response_model=TicketResponse)
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


@router.get("/{ticket_id}", response_model=TicketResponse)
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

    if ticket.requester_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este chamado",
        )

    return ticket

@router.patch("/{ticket_id}", response_model=TicketResponse)
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
    
    if ticket.requester_id != current_user.id:
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

@router.get("/", response_model=list[TicketResponse])
def list_tickets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tickets = db.scalars(
        select(Ticket)
        .where(Ticket.requester_id == current_user.id)
        .order_by(Ticket.id.desc())
    ).all()

    return tickets