"""
WebSocket endpoint for real-time collaboration
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.services.ws import manager
# We are making token optional for now, and we will not authenticate in development
# In production, we would want to authenticate the user via the token.
from app.db.session import get_db
from sqlalchemy.orm import Session
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/{project_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    project_id: int,
    token: str = None,  # Optional token for development
    db: Session = Depends(get_db),
):
    # For now, we are not authenticating via token in development.
    # In a production environment, you would validate the token and get the user.
    # We'll skip the authentication for now to keep the example simple and focused on the WebSocket feature.
    # However, note that in a real app, you would want to authenticate the user and check if they have access to the project.

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Expecting JSON data with at least a 'type' field
            try:
                message = json.loads(data)
                # Broadcast the message to all connected clients for this project
                # In a more advanced implementation, we would filter by project_id
                await manager.broadcast(json.dumps({
                    "project_id": project_id,
                    "message": message
                }))
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({"error": "Invalid JSON"}))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"WebSocket disconnected for project {project_id}")