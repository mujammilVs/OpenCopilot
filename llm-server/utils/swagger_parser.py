from entities.action_entity import ActionDTO


class Endpoint:
    def __init__(self, operation_id, endpoint_type, name, description, request_body, request_parameters, response,
                 path):
        self.operation_id = operation_id
        self.type = endpoint_type
        self.name = name
        self.description = description
        self.request_body = request_body
        self.request_parameters = request_parameters
        self.response = response
        self.path = path

    def to_dict(self):
        return {
            "operation_id": self.operation_id,
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "request_body": self.request_body,
            "request_parameters": self.request_parameters,
            "response": self.response,
            "path": self.path
        }


def get_post_endpoints_without_request_body(endpoints):
    return [endpoint for endpoint in endpoints if endpoint.type == 'POST' and not endpoint.request_body]


def get_endpoints_without_name(endpoints):
    return [endpoint for endpoint in endpoints if not endpoint.name]


def get_endpoints_without_description(endpoints):
    return [endpoint for endpoint in endpoints if not endpoint.description]


def get_endpoints_without_operation_id(endpoints):
    return [endpoint for endpoint in endpoints if not endpoint.operation_id]


class SwaggerParser:
    NONE = 'none'
    API_KEY = 'apiKey'
    HTTP = 'http'
    OAUTH2 = 'oauth2'

    def __init__(self, content):
        self.swagger_data = content
        if self.swagger_data is None:
            raise Exception("Failed to parse Swagger file")

    def get_version(self):
        return self.swagger_data.get('openapi')

    def get_title(self):
        return self.swagger_data.get('info', {}).get('title')

    def get_description(self):
        return self.swagger_data.get('info', {}).get('description')

    def get_swagger_data(self):
        return self.swagger_data

    def get_endpoints(self):
        endpoints = []
        paths = self.swagger_data.get('paths', {})

        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                endpoint = Endpoint(
                    operation_id=method_data.get('operationId'),
                    endpoint_type=method.upper(),
                    name=method_data.get('summary'),
                    description=method_data.get('description'),
                    request_body=method_data.get('requestBody'),
                    request_parameters=method_data.get('parameters'),
                    response=method_data.get('responses'),
                    path=path
                )
                endpoints.append(endpoint)

        return endpoints

    def get_authorization_type(self):
        security_schemes = self.swagger_data.get('components', {}).get('securitySchemes', {})
        for name, security_scheme in security_schemes.items():
            scheme_type = security_scheme.get('type')
            if scheme_type in [self.NONE, self.API_KEY, self.HTTP, self.OAUTH2]:
                return scheme_type
        return None

    def get_validations(self):
        endpoints = self.get_endpoints()
        validations = {
            'endpoints_without_operation_id': [endpoint.to_dict() for endpoint in
                                               get_endpoints_without_operation_id(endpoints)],
            'endpoints_without_description': [endpoint.to_dict() for endpoint in
                                              get_endpoints_without_description(endpoints)],
            'endpoints_without_name': [endpoint.to_dict() for endpoint in get_endpoints_without_name(endpoints)],
            'auth_type': self.get_authorization_type()
        }
        return validations

    def get_base_uri(self):
        """
        Retrieves the base URI from the Swagger file's "servers" object, specific to OpenAPI 3.0.0.
        """
        servers = self.swagger_data.get('servers', [])
        if servers:
            # Use the first server's URL as the base URI
            return servers[0].get('url', '')
        return ''

    def get_all_actions(self):
        """
        Retrieves all actions defined in the Swagger file as ActionDTO instances.
        Each action represents an operation (GET, POST, PUT, etc.) on a path and includes details like base_uri,
        path, name, summary, operation_id, and other relevant information.
        """
        actions = []
        base_uri = self.get_base_uri()
        paths = self.swagger_data.get('paths', {})

        for path, path_data in paths.items():
            for method, method_data in path_data.items():
                payload = {
                    "request_body": method_data.get('requestBody'),
                    "request_parameters": method_data.get('parameters'),
                    "response": method_data.get('responses')
                }

                action_dto = ActionDTO(
                    base_uri=base_uri,
                    path=path,
                    name=method_data.get('summary'),
                    description=method_data.get('description'),
                    operation_id=method_data.get('operationId'),
                    request_type=method.upper(),
                    payload=payload,
                )
                actions.append(action_dto)

        return actions
