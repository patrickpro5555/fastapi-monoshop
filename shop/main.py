from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from dependencies import get_db, templates, env
from shop import crud
from shop.models import Category

router = APIRouter(prefix="/products")


@router.get("/{category_slug}")
def product_list(
    request: Request, category_slug: str, page: int = 1, db: Session = Depends(get_db)
):
    products = crud.product_list(db=db, category_slug=category_slug)
    categories = db.query(Category).all()[16 * (page - 1) : 16 * (page)]
    category = db.query(Category).filter_by(slug=category_slug).first()

    template = env.get_template("list.html")

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "page": page,
            "products": jsonable_encoder(products),
            "categories": jsonable_encoder(categories),
            "category": jsonable_encoder(category),
        },
    )
