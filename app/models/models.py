from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Enum, Table, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.database import Base

# Association table for many-to-many relationship between users and families
user_family = Table(
    'user_family',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('family_id', Integer, ForeignKey('families.id'))
)

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"

class TransactionCategory(str, enum.Enum):
    # Income Categories
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    RENTAL = "rental"
    BUSINESS = "business"
    OTHER_INCOME = "other_income"
    
    # Expense Categories
    FOOD = "food"
    TRANSPORT = "transport"
    HOUSING = "housing"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTH = "health"
    EDUCATION = "education"
    SHOPPING = "shopping"
    TRAVEL = "travel"
    SUBSCRIPTIONS = "subscriptions"
    DEBT_PAYMENT = "debt_payment"
    OTHER_EXPENSE = "other_expense"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)  # Может быть null для Apple auth
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(UserRole), default=UserRole.MEMBER)
    apple_id = Column(String, unique=True, nullable=True)  # ID пользователя от Apple
    
    # Relationships
    families = relationship("Family", secondary=user_family, back_populates="members")
    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    accounts = relationship("Account", back_populates="user")

class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    members = relationship("User", secondary=user_family, back_populates="families")
    transactions = relationship("Transaction", back_populates="family")
    budgets = relationship("Budget", back_populates="family")
    goals = relationship("FinancialGoal", back_populates="family")
    accounts = relationship("Account", back_populates="family")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # checking, savings, credit_card, cash, investment
    balance = Column(Float, default=0)
    currency = Column(String, default="USD")
    user_id = Column(Integer, ForeignKey("users.id"))
    family_id = Column(Integer, ForeignKey("families.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    family = relationship("Family", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(TransactionType))
    amount = Column(Float)
    description = Column(String)
    category = Column(Enum(TransactionCategory))
    date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    family_id = Column(Integer, ForeignKey("families.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
    has_items = Column(Boolean, default=False)
    items_details = Column(JSON)  # Stores items information
    recurring = Column(Boolean, default=False)
    recurring_details = Column(JSON)  # Stores recurring transaction details
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    family = relationship("Family", back_populates="transactions")
    account = relationship("Account", back_populates="transactions")
    items = relationship("TransactionItem", back_populates="transaction")

class TransactionItem(Base):
    __tablename__ = "transaction_items"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    amount = Column(Float)
    category = Column(Enum(TransactionCategory))
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  # Who this item belongs to
    
    # Relationships
    transaction = relationship("Transaction", back_populates="items")
    user = relationship("User")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(TransactionCategory))
    amount = Column(Float)
    period = Column(String)  # monthly, weekly, yearly
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    family_id = Column(Integer, ForeignKey("families.id"))
    
    # Relationships
    user = relationship("User", back_populates="budgets")
    family = relationship("Family", back_populates="budgets")

class FinancialGoal(Base):
    __tablename__ = "financial_goals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    target_amount = Column(Float)
    current_amount = Column(Float, default=0)
    deadline = Column(DateTime)
    family_id = Column(Integer, ForeignKey("families.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    family = relationship("Family", back_populates="goals")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    type = Column(String)  # budget_alert, goal_achieved, etc.
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow) 