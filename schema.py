task_list_schema = {
    'type': 'object',
    'properties': {
        'tasks': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'priority': {'type': 'string'},
                    'completed': {'type': 'boolean'},
                    'due_date': {'type': ['string', 'null']},
                    'tags': {'type': 'array', 'items': {'type': 'string'}},
                    'subtasks': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'title': {'type': 'string'},
                                'completed': {'type': 'boolean'}
                            },
                            'required': ['title', 'completed']
                        }
                    }
                },
                'required': ['title', 'priority', 'completed']
            }
        }
    },
    'required': ['tasks']
}
