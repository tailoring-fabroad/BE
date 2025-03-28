from src.app.models import RWModel

class RWSchema(RWModel):
    model_config = {
        **RWModel.model_config,
        "from_attributes": True
    }
