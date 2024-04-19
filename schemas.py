from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True #changed to orm to from attribute
        from_attributes:True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True #changed to orm to from attribute
        from_attributes:True   





class UserUpdate(BaseModel):
    email: str
    # Add other fields you want to allow updating here

class ItemBaseUpdate(BaseModel):
    title: str
    description: str | None = None


class UserBaseUpdate(BaseModel):
    email: str


class ItemDelete(BaseModel):
    id: int


class UserDelete(BaseModel):
    id: int
