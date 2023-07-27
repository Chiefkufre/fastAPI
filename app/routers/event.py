from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter

# Internal Imports
from models import Event, User
from schemas import *
from database import engine, Base, get_db
from utils import generate_hash
import oauth2

# Sqlalchemy import
from sqlalchemy.orm import Session


router = APIRouter(prefix="/events", tags=["Events"])
# create events
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)):


    print(type(current_user))
    new_event = Event(
        **event.dict()
        # event_name=event.name, venue=event.venue, description=event.description
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return {"created": new_event}


# read all events
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[EventRead])
def get_events(db: Session = Depends(get_db)):

    query_event = db.query(Event).all()

    if query_event == None:
        return HTTPException(
            status_code==status.HTTP_204_NO_CONTENT,
            detail="No event found. Don't worry, you can add yours")
    return query_event


# Read events by id
@router.get("/{id}", response_model = EventRead)
def get_events_by_id(id: int, db: Session = Depends(get_db)):

    query_event = db.query(Event).filter(Event.id == id)

    event = query_event.first()
    if event == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post with the id not found"
        )
    else:
        return event



@router.delete("/{id}")
def delete_event(id: int, db: Session = Depends(get_db),  current_user: int = Depends(oauth2.get_current_user)):
    eventt = db.query(Event).filter(Event.id == id)

    event = eventt.first()

    if event == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"event with the id:{id} not found"
        )
    
    # if event.user_id != user_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"not authorized to perform this operation"
    #     )
    eventt.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_event(id: int, event: EventUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    eventt = db.query(Event).filter(Event.id == id)

    eventtt = eventt.first()

    if eventtt == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post with the id not found"
        )

    if eventtt.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorized to perform this operation"
        )
    eventt.update(
        event.dict(),
        synchronize_session=False,
    )
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
