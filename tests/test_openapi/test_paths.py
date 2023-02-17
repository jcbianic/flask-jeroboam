from flask.testing import FlaskClient


unspported_use_case = {
    "/non_decorated_route": {
        "get": {
            "responses": {
                "200": {
                    "description": "Successful Response",
                    "content": {"application/json": {"schema": {}}},
                }
            },
            "summary": "Non Decorated Route",
            "operationId": "non_decorated_route_non_decorated_route_get",
        }
    }
}

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/api_route": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Non Operation",
                "operationId": "get_non_operation",
                "tags": ["Base"],
            }
        },
        "/text": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Get Text",
                "operationId": "get_text",
                "tags": ["Base"],
            }
        },
        "/path/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Id",
                "operationId": "path_params_router_get_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/str/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Str Id",
                "operationId": "path_params_router_get_str_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Int Id",
                "operationId": "path_params_router_get_int_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "integer"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/float/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Float Id",
                "operationId": "path_params_router_get_float_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "number"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/bool/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Bool Id",
                "operationId": "path_params_router_get_bool_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "boolean"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Id",
                "operationId": "path_params_router_get_path_param_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-required/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Required Id",
                "operationId": "path_params_router_get_path_param_required_id",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Item Id", "type": "string"},
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-minlength/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Min Length",
                "operationId": "path_params_router_get_path_param_min_length",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "minLength": 3,
                            "type": "string",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-maxlength/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Max Length",
                "operationId": "path_params_router_get_path_param_max_length",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maxLength": 3,
                            "type": "string",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-min_maxlength/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Min Max Length",
                "operationId": "path_params_router_get_path_param_min_max_length",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maxLength": 3,
                            "minLength": 2,
                            "type": "string",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-gt/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Gt",
                "operationId": "path_params_router_get_path_param_gt",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMinimum": 3.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-gt0/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Gt0",
                "operationId": "path_params_router_get_path_param_gt0",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMinimum": 0.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-ge/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Ge",
                "operationId": "path_params_router_get_path_param_ge",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "minimum": 3.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-lt/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Lt",
                "operationId": "path_params_router_get_path_param_lt",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMaximum": 3.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-lt0/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Lt0",
                "operationId": "path_params_router_get_path_param_lt0",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMaximum": 0.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-le/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Le",
                "operationId": "path_params_router_get_path_param_le",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maximum": 3.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-lt-gt/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Lt Gt",
                "operationId": "path_params_router_get_path_param_lt_gt",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMaximum": 3.0,
                            "exclusiveMinimum": 1.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-le-ge/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Le Ge",
                "operationId": "path_params_router_get_path_param_le_ge",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maximum": 3.0,
                            "minimum": 1.0,
                            "type": "number",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-lt-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Lt Int",
                "operationId": "path_params_router_get_path_param_lt_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMaximum": 3.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-gt-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Gt Int",
                "operationId": "path_params_router_get_path_param_gt_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMinimum": 3.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-le-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Le Int",
                "operationId": "path_params_router_get_path_param_le_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maximum": 3.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-ge-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Ge Int",
                "operationId": "path_params_router_get_path_param_ge_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "minimum": 3.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-lt-gt-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Lt Gt Int",
                "operationId": "path_params_router_get_path_param_lt_gt_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "exclusiveMaximum": 3.0,
                            "exclusiveMinimum": 1.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/path/param-le-ge-int/{item_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Path Param Le Ge Int",
                "operationId": "path_params_router_get_path_param_le_ge_int",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Item Id",
                            "maximum": 3.0,
                            "minimum": 1.0,
                            "type": "integer",
                        },
                        "name": "item_id",
                        "in": "path",
                    }
                ],
                "tags": ["Path"],
            }
        },
        "/query": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query",
                "operationId": "query_params_router_get_query",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Query"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/optional": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Optional",
                "operationId": "query_params_router_get_query_optional",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Query"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/int": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Type",
                "operationId": "query_params_router_get_query_type",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Query", "type": "integer"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/int/optional": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Type Optional",
                "operationId": "query_params_router_get_query_type_optional",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Query", "type": "integer"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/int/default": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Type Int Default",
                "operationId": "query_params_router_get_query_type_int_default",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Query", "type": "integer", "default": 10},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/param": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Param",
                "operationId": "query_params_router_get_query_param",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Query"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/param-required": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Param Required",
                "operationId": "query_params_router_get_query_param_required",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Query"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/query/param-required/int": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "summary": "Get Query Param Required Type",
                "operationId": "query_params_router_get_query_param_required_type",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Query", "type": "integer"},
                        "name": "query",
                        "in": "query",
                    }
                ],
                "tags": ["Query"],
            }
        },
        "/enum-status-code": {
            "get": {
                "responses": {
                    "201": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                },
                "summary": "Get Enum Status Code",
                "operationId": "query_params_router_get_enum_status_code",
                "tags": ["Query"],
            }
        },
        "/query/frozenset": {
            "get": {
                "summary": "Get Query Type Frozenset",
                "operationId": "query_params_router_get_query_type_frozenset",
                "parameters": [
                    {
                        "required": True,
                        "schema": {
                            "title": "Query",
                            "uniqueItems": True,
                            "type": "array",
                            "items": {"type": "integer"},
                        },
                        "name": "query",
                        "in": "query",
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                    "400": {
                        "description": "Validation Error",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                    },
                },
                "tags": ["Query"],
            }
        },
    },
    "components": {
        "schemas": {
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
            "HTTPValidationError": {
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
        }
    },
}


def test_paths_item(client: FlaskClient):
    """Test info endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return_shema = response.json
    assert return_shema
    for path in openapi_schema["paths"].keys():  # type: ignore
        assert (
            return_shema["paths"][path] == openapi_schema["paths"][path]  # type: ignore
        ), f"{path} don't match"


def test_error_schemas(client: FlaskClient):
    """Test info endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    return_schema = response.json
    target_schema = openapi_schema["components"]["schemas"]  # type: ignore
    assert return_schema
    assert (
        return_schema["components"]["schemas"]["HTTPValidationError"]  # type: ignore
        == target_schema["HTTPValidationError"]  # type: ignore
    )
    assert (
        return_schema["components"]["schemas"]["ValidationError"]  # type: ignore
        == target_schema["ValidationError"]  # type: ignore
    )
