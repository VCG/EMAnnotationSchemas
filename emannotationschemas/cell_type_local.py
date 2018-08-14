from emannotationschemas.base import BoundSpatialPoint, AnnotationSchema
import marshmallow as mm
from marshmallow.validate import Range, OneOf

allowed_classification_systems = ['ivscc',
                             'valence',
                             'classical',
                             'freeform']

allowed_types = dict(
                    valence=['e',
                             'i',
                             'g',
                             'unknown'],
                    ivscc=[ 'spiny_{}'.format(i) for i in range(1,15) ] + \
                          [ 'aspiny_s_{}'.format(i) for i in range(1,17) ] + \
                          [ 'unknown' ],
                    classical=['chandelier',
                             'pyramidal',
                             'martinotti',
                             'pv',
                             'sst',
                             'vip',
                             'neurogliaform',
                             'unknown',
                             'astrocyte',
                             'microglia-perivascular',
                             'microglia-perineuronal',
                             'unknown'
                             ]
                    )

class CellTypeLocal( AnnotationSchema ):

    classification_system = mm.fields.String(
                            required=True,
                            description='Classification system followed',
                            validate=OneOf( allowed_classification_systems ))
    cell_type = mm.fields.String(
                            required=True,
                            description='Cell type name')
    confidence = mm.fields.Float(
                            required=False,
                            description='Confidence in assignment, between 0-1',
                            validate=Range(min=0,max=1) )
    pt = mm.fields.Nested( BoundSpatialPoint, 
                            required=True,
                            description='Location associated with classification')
    @mm.post_load
    def validate_type( self, item):
        assert item['type'] == 'cell_type'

        system = item['classification_system']
        if system in allowed_types.keys(): 
            if item['cell_type'] not in allowed_types[system]:
                item['valid'] = False
            else:
                item['valid'] = True
        else:
            item['valid'] = True

        return item