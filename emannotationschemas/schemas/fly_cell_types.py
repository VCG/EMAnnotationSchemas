import marshmallow as mm
from marshmallow.validate import OneOf
from emannotationschemas.schemas.base import (
    AnnotationSchema,
    BoundSpatialPoint,
    ReferenceAnnotation,
)

allowed_hemispheres = ["L", "R", "M", "U"]


class FlyCellType(AnnotationSchema):

    classification_system = mm.fields.String(
        required=True, description="Classification system followed"
    )
    pt = mm.fields.Nested(
        BoundSpatialPoint,
        required=True,
        description="Location associated with classification",
    )
    cell_type = mm.fields.String(required=True, description="Cell type name")
    hemisphere = mm.field.String(
        required=True,
        default="U",
        description="Cell hemisphere",
        validate=OneOf(allowed_hemispheres),
    )


class FlyCellTypeExt(FlyCellType):
    driver_line = mm.fields.String(required=False, description="Driver line name")
    synonym = mm.fields.String(required=False, description="Synonym")
