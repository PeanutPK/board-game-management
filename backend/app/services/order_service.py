"""Order business logic and interactions with the database focus on stock updates and payment simulation."""
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.booking import Order
from app.schemas.ordering_schema import OrderCreate
from app.services.game_service import GameService


class OrderService:
    """Service for order operations."""
    
    @staticmethod
    def create_order(db: Session, user_id: int, order: OrderCreate) -> Order:
        """Create a new order."""
        # Check stock
        game = GameService.get_game(db, order.game_id)
        if not GameService.check_stock(db, order.game_id, order.quantity):
            raise HTTPException(status_code=400, detail="Insufficient stock")
        
        # Calculate total price
        total_price = int(game.price * 100 * order.quantity)  # Store in cents
        
        # Create order
        db_order = Order(
            user_id=user_id,
            game_id=order.game_id,
            quantity=order.quantity,
            total_price=total_price,
            status="pending"
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        """Get order by ID."""
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
    @staticmethod
    def get_user_orders(db: Session, user_id: int) -> list[Order]:
        """Get all orders for a user."""
        return db.query(Order).filter(Order.user_id == user_id).all()
    
    @staticmethod
    def complete_order(db: Session, order_id: int) -> Order:
        """Mark an order as completed (after payment)."""
        order = OrderService.get_order(db, order_id)
        order.status = "completed"
        
        # Deduct from stock
        game = GameService.get_game(db, order.game_id)
        game.stock -= order.quantity
        
        db.add(order)
        db.add(game)
        db.commit()
        db.refresh(order)
        return order