from pydantic import BaseModel
from typing import List


class ReportOut(BaseModel):
    id: int
    title: str
    status: str


class AdminDataOut(BaseModel):
    name: str
    email: str
    reports: List[ReportOut]


class AdminOut(BaseModel):
    message: str
    data: AdminDataOut


class Purchase(BaseModel):
    id: int
    item: str
    price: float


class UserData(BaseModel):
    name: str
    email: str
    purchases: List[Purchase]


class UserOut(BaseModel):
    message: str
    data: UserData
