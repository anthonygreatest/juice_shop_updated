from pydantic import BaseModel, Field



class AddToBasketRequestSchema(BaseModel):
    product_id: int |str = Field(alias='ProductId')
    quantity: int
    basket_id: int | str = Field(alias='BasketId')


    model_config = {
        "populate_by_name": True
    }