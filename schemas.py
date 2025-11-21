"""
Database Schemas for Garden Services App

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercase of the class name, e.g., Service -> "service".
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import date


class Provider(BaseModel):
    name: str = Field(..., description="Provider full name or business name")
    email: Optional[EmailStr] = Field(None, description="Contact email")
    phone: Optional[str] = Field(None, description="Contact phone number")
    service_areas: Optional[List[str]] = Field(default=None, description="Cities/areas covered")
    rating: Optional[float] = Field(default=None, ge=0, le=5, description="Average rating 0-5")
    is_active: bool = Field(default=True)


class Service(BaseModel):
    title: str = Field(..., description="Service name, e.g., Lawn Mowing")
    description: Optional[str] = Field(None, description="Short description of the service")
    base_price: Optional[float] = Field(None, ge=0, description="Starting price in dollars")
    category: Optional[str] = Field(None, description="Category like maintenance, design, cleanup")
    duration_estimate_min: Optional[int] = Field(None, ge=0, description="Estimated duration in minutes")
    is_active: bool = Field(default=True)


class ServiceRequest(BaseModel):
    customer_name: str = Field(...)
    customer_email: EmailStr = Field(...)
    customer_phone: Optional[str] = Field(None)
    address: str = Field(...)
    service_title: str = Field(..., description="Title of the requested service")
    preferred_date: Optional[date] = Field(None)
    notes: Optional[str] = Field(None)
    status: str = Field("pending", description="pending | confirmed | completed | cancelled")


class Review(BaseModel):
    provider_id: str = Field(..., description="Referenced provider id as string")
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    customer_name: Optional[str] = None
