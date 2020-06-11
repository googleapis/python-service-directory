# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.servicedirectory_v1beta1.services.registration_service import (
    RegistrationServiceClient,
)
from google.cloud.servicedirectory_v1beta1.services.registration_service import pagers
from google.cloud.servicedirectory_v1beta1.services.registration_service import (
    transports,
)
from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import options_pb2 as options  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.type import expr_pb2 as expr  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert RegistrationServiceClient._get_default_mtls_endpoint(None) is None
    assert (
        RegistrationServiceClient._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegistrationServiceClient._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        RegistrationServiceClient._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegistrationServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        RegistrationServiceClient._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_registration_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = RegistrationServiceClient.from_service_account_file(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        client = RegistrationServiceClient.from_service_account_json(
            "dummy/file/path.json"
        )
        assert client._transport._credentials == creds

        assert client._transport._host == "servicedirectory.googleapis.com:443"


def test_registration_service_client_get_transport_class():
    transport = RegistrationServiceClient.get_transport_class()
    assert transport == transports.RegistrationServiceGrpcTransport

    transport = RegistrationServiceClient.get_transport_class("grpc")
    assert transport == transports.RegistrationServiceGrpcTransport


def test_registration_service_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.RegistrationServiceClient.get_transport_class"
    ) as gtc:
        transport = transports.RegistrationServiceGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = RegistrationServiceClient(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.RegistrationServiceClient.get_transport_class"
    ) as gtc:
        client = RegistrationServiceClient(transport="grpc")
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistrationServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "never".
    os.environ["GOOGLE_API_USE_MTLS"] = "never"
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistrationServiceClient()
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_ENDPOINT,
            client_cert_source=None,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS is
    # "always".
    os.environ["GOOGLE_API_USE_MTLS"] = "always"
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistrationServiceClient()
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=None,
            credentials=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistrationServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_MTLS_ENDPOINT,
        )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", and default_client_cert_source is provided.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=True,
        ):
            grpc_transport.return_value = None
            client = RegistrationServiceClient()
            grpc_transport.assert_called_once_with(
                api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
                client_cert_source=None,
                credentials=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
            )

    # Check the case api_endpoint is not provided, GOOGLE_API_USE_MTLS is
    # "auto", but client_cert_source and default_client_cert_source are None.
    os.environ["GOOGLE_API_USE_MTLS"] = "auto"
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        with mock.patch(
            "google.auth.transport.mtls.has_default_client_cert_source",
            return_value=False,
        ):
            grpc_transport.return_value = None
            client = RegistrationServiceClient()
            grpc_transport.assert_called_once_with(
                api_mtls_endpoint=client.DEFAULT_ENDPOINT,
                client_cert_source=None,
                credentials=None,
                host=client.DEFAULT_ENDPOINT,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS has
    # unsupported value.
    os.environ["GOOGLE_API_USE_MTLS"] = "Unsupported"
    with pytest.raises(MutualTLSChannelError):
        client = RegistrationServiceClient()

    del os.environ["GOOGLE_API_USE_MTLS"]


def test_registration_service_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.servicedirectory_v1beta1.services.registration_service.transports.RegistrationServiceGrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = RegistrationServiceClient(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_create_namespace(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.CreateNamespaceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_namespace.Namespace(name="name_value")

        response = client.create_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_namespace.Namespace)
    assert response.name == "name_value"


def test_create_namespace_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.CreateNamespaceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_namespace), "__call__"
    ) as call:
        call.return_value = gcs_namespace.Namespace()

        client.create_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_create_namespace_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.create_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_namespace.Namespace()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_namespace(
            parent="parent_value",
            namespace=gcs_namespace.Namespace(name="name_value"),
            namespace_id="namespace_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].namespace == gcs_namespace.Namespace(name="name_value")
        assert args[0].namespace_id == "namespace_id_value"


def test_create_namespace_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_namespace(
            registration_service.CreateNamespaceRequest(),
            parent="parent_value",
            namespace=gcs_namespace.Namespace(name="name_value"),
            namespace_id="namespace_id_value",
        )


def test_list_namespaces(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.ListNamespacesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_namespaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListNamespacesResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_namespaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListNamespacesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_namespaces_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.ListNamespacesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_namespaces), "__call__") as call:
        call.return_value = registration_service.ListNamespacesResponse()

        client.list_namespaces(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_namespaces_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_namespaces), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListNamespacesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_namespaces(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_namespaces_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_namespaces(
            registration_service.ListNamespacesRequest(), parent="parent_value"
        )


def test_list_namespaces_pager():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_namespaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListNamespacesResponse(
                namespaces=[
                    namespace.Namespace(),
                    namespace.Namespace(),
                    namespace.Namespace(),
                ],
                next_page_token="abc",
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[], next_page_token="def"
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[namespace.Namespace()], next_page_token="ghi"
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[namespace.Namespace(), namespace.Namespace()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_namespaces(request={})]
        assert len(results) == 6
        assert all(isinstance(i, namespace.Namespace) for i in results)


def test_list_namespaces_pages():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_namespaces), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListNamespacesResponse(
                namespaces=[
                    namespace.Namespace(),
                    namespace.Namespace(),
                    namespace.Namespace(),
                ],
                next_page_token="abc",
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[], next_page_token="def"
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[namespace.Namespace()], next_page_token="ghi"
            ),
            registration_service.ListNamespacesResponse(
                namespaces=[namespace.Namespace(), namespace.Namespace()]
            ),
            RuntimeError,
        )
        pages = list(client.list_namespaces(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_namespace(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.GetNamespaceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_namespace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = namespace.Namespace(name="name_value")

        response = client.get_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, namespace.Namespace)
    assert response.name == "name_value"


def test_get_namespace_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.GetNamespaceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_namespace), "__call__") as call:
        call.return_value = namespace.Namespace()

        client.get_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_namespace_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_namespace), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = namespace.Namespace()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_namespace(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_namespace_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_namespace(
            registration_service.GetNamespaceRequest(), name="name_value"
        )


def test_update_namespace(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.UpdateNamespaceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_namespace.Namespace(name="name_value")

        response = client.update_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_namespace.Namespace)
    assert response.name == "name_value"


def test_update_namespace_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.UpdateNamespaceRequest()
    request.namespace.name = "namespace.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_namespace), "__call__"
    ) as call:
        call.return_value = gcs_namespace.Namespace()

        client.update_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "namespace.name=namespace.name/value") in kw[
        "metadata"
    ]


def test_update_namespace_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.update_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_namespace.Namespace()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_namespace(
            namespace=gcs_namespace.Namespace(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].namespace == gcs_namespace.Namespace(name="name_value")
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_namespace_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_namespace(
            registration_service.UpdateNamespaceRequest(),
            namespace=gcs_namespace.Namespace(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_namespace(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.DeleteNamespaceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_namespace_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.DeleteNamespaceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_namespace), "__call__"
    ) as call:
        call.return_value = None

        client.delete_namespace(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_delete_namespace_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.delete_namespace), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_namespace(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_namespace_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_namespace(
            registration_service.DeleteNamespaceRequest(), name="name_value"
        )


def test_create_service(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.CreateServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_service.Service(name="name_value")

        response = client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_service.Service)
    assert response.name == "name_value"


def test_create_service_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.CreateServiceRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        call.return_value = gcs_service.Service()

        client.create_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_create_service_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_service(
            parent="parent_value",
            service=gcs_service.Service(name="name_value"),
            service_id="service_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].service == gcs_service.Service(name="name_value")
        assert args[0].service_id == "service_id_value"


def test_create_service_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_service(
            registration_service.CreateServiceRequest(),
            parent="parent_value",
            service=gcs_service.Service(name="name_value"),
            service_id="service_id_value",
        )


def test_list_services(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.ListServicesRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListServicesResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListServicesPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_services_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.ListServicesRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        call.return_value = registration_service.ListServicesResponse()

        client.list_services(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_services_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListServicesResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_services(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_services_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_services(
            registration_service.ListServicesRequest(), parent="parent_value"
        )


def test_list_services_pager():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service()],
                next_page_token="abc",
            ),
            registration_service.ListServicesResponse(
                services=[], next_page_token="def"
            ),
            registration_service.ListServicesResponse(
                services=[service.Service()], next_page_token="ghi"
            ),
            registration_service.ListServicesResponse(
                services=[service.Service(), service.Service()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_services(request={})]
        assert len(results) == 6
        assert all(isinstance(i, service.Service) for i in results)


def test_list_services_pages():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_services), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListServicesResponse(
                services=[service.Service(), service.Service(), service.Service()],
                next_page_token="abc",
            ),
            registration_service.ListServicesResponse(
                services=[], next_page_token="def"
            ),
            registration_service.ListServicesResponse(
                services=[service.Service()], next_page_token="ghi"
            ),
            registration_service.ListServicesResponse(
                services=[service.Service(), service.Service()]
            ),
            RuntimeError,
        )
        pages = list(client.list_services(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_service(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.GetServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.Service(name="name_value")

        response = client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.Service)
    assert response.name == "name_value"


def test_get_service_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.GetServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        call.return_value = service.Service()

        client.get_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_service_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_service(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_service_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_service(registration_service.GetServiceRequest(), name="name_value")


def test_update_service(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.UpdateServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_service.Service(name="name_value")

        response = client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_service.Service)
    assert response.name == "name_value"


def test_update_service_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.UpdateServiceRequest()
    request.service.name = "service.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        call.return_value = gcs_service.Service()

        client.update_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "service.name=service.name/value") in kw[
        "metadata"
    ]


def test_update_service_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_service.Service()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_service(
            service=gcs_service.Service(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].service == gcs_service.Service(name="name_value")
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_service_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_service(
            registration_service.UpdateServiceRequest(),
            service=gcs_service.Service(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_service(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.DeleteServiceRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_service_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.DeleteServiceRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        call.return_value = None

        client.delete_service(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_delete_service_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_service), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_service(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_service_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_service(
            registration_service.DeleteServiceRequest(), name="name_value"
        )


def test_create_endpoint(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.CreateEndpointRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_endpoint.Endpoint(
            name="name_value", address="address_value", port=453
        )

        response = client.create_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_endpoint.Endpoint)
    assert response.name == "name_value"
    assert response.address == "address_value"
    assert response.port == 453


def test_create_endpoint_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.CreateEndpointRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_endpoint), "__call__") as call:
        call.return_value = gcs_endpoint.Endpoint()

        client.create_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_create_endpoint_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.create_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_endpoint.Endpoint()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_endpoint(
            parent="parent_value",
            endpoint=gcs_endpoint.Endpoint(name="name_value"),
            endpoint_id="endpoint_id_value",
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"
        assert args[0].endpoint == gcs_endpoint.Endpoint(name="name_value")
        assert args[0].endpoint_id == "endpoint_id_value"


def test_create_endpoint_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_endpoint(
            registration_service.CreateEndpointRequest(),
            parent="parent_value",
            endpoint=gcs_endpoint.Endpoint(name="name_value"),
            endpoint_id="endpoint_id_value",
        )


def test_list_endpoints(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.ListEndpointsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_endpoints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListEndpointsResponse(
            next_page_token="next_page_token_value"
        )

        response = client.list_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListEndpointsPager)
    assert response.next_page_token == "next_page_token_value"


def test_list_endpoints_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.ListEndpointsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_endpoints), "__call__") as call:
        call.return_value = registration_service.ListEndpointsResponse()

        client.list_endpoints(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value") in kw["metadata"]


def test_list_endpoints_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_endpoints), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = registration_service.ListEndpointsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_endpoints(parent="parent_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == "parent_value"


def test_list_endpoints_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_endpoints(
            registration_service.ListEndpointsRequest(), parent="parent_value"
        )


def test_list_endpoints_pager():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_endpoints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListEndpointsResponse(
                endpoints=[
                    endpoint.Endpoint(),
                    endpoint.Endpoint(),
                    endpoint.Endpoint(),
                ],
                next_page_token="abc",
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[], next_page_token="def"
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[endpoint.Endpoint()], next_page_token="ghi"
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[endpoint.Endpoint(), endpoint.Endpoint()]
            ),
            RuntimeError,
        )
        results = [i for i in client.list_endpoints(request={})]
        assert len(results) == 6
        assert all(isinstance(i, endpoint.Endpoint) for i in results)


def test_list_endpoints_pages():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.list_endpoints), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            registration_service.ListEndpointsResponse(
                endpoints=[
                    endpoint.Endpoint(),
                    endpoint.Endpoint(),
                    endpoint.Endpoint(),
                ],
                next_page_token="abc",
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[], next_page_token="def"
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[endpoint.Endpoint()], next_page_token="ghi"
            ),
            registration_service.ListEndpointsResponse(
                endpoints=[endpoint.Endpoint(), endpoint.Endpoint()]
            ),
            RuntimeError,
        )
        pages = list(client.list_endpoints(request={}).pages)
        for page, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page.raw_page.next_page_token == token


def test_get_endpoint(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.GetEndpointRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint.Endpoint(
            name="name_value", address="address_value", port=453
        )

        response = client.get_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, endpoint.Endpoint)
    assert response.name == "name_value"
    assert response.address == "address_value"
    assert response.port == 453


def test_get_endpoint_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.GetEndpointRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_endpoint), "__call__") as call:
        call.return_value = endpoint.Endpoint()

        client.get_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_get_endpoint_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = endpoint.Endpoint()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_endpoint(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_get_endpoint_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_endpoint(
            registration_service.GetEndpointRequest(), name="name_value"
        )


def test_update_endpoint(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.UpdateEndpointRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_endpoint.Endpoint(
            name="name_value", address="address_value", port=453
        )

        response = client.update_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gcs_endpoint.Endpoint)
    assert response.name == "name_value"
    assert response.address == "address_value"
    assert response.port == 453


def test_update_endpoint_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.UpdateEndpointRequest()
    request.endpoint.name = "endpoint.name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_endpoint), "__call__") as call:
        call.return_value = gcs_endpoint.Endpoint()

        client.update_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "endpoint.name=endpoint.name/value") in kw[
        "metadata"
    ]


def test_update_endpoint_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.update_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = gcs_endpoint.Endpoint()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_endpoint(
            endpoint=gcs_endpoint.Endpoint(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].endpoint == gcs_endpoint.Endpoint(name="name_value")
        assert args[0].update_mask == field_mask.FieldMask(paths=["paths_value"])


def test_update_endpoint_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_endpoint(
            registration_service.UpdateEndpointRequest(),
            endpoint=gcs_endpoint.Endpoint(name="name_value"),
            update_mask=field_mask.FieldMask(paths=["paths_value"]),
        )


def test_delete_endpoint(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = registration_service.DeleteEndpointRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_endpoint_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = registration_service.DeleteEndpointRequest()
    request.name = "name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_endpoint), "__call__") as call:
        call.return_value = None

        client.delete_endpoint(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "name=name/value") in kw["metadata"]


def test_delete_endpoint_flattened():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.delete_endpoint), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_endpoint(name="name_value")

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == "name_value"


def test_delete_endpoint_flattened_error():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_endpoint(
            registration_service.DeleteEndpointRequest(), name="name_value"
        )


def test_get_iam_policy(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.GetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_get_iam_policy_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.GetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.get_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_get_iam_policy_from_dict():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.get_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.get_iam_policy(
            request={
                "resource": "resource_value",
                "options": options.GetPolicyOptions(requested_policy_version=2598),
            }
        )
        call.assert_called()


def test_set_iam_policy(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.SetIamPolicyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy(version=774, etag=b"etag_blob")

        response = client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, policy.Policy)
    assert response.version == 774
    assert response.etag == b"etag_blob"


def test_set_iam_policy_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.SetIamPolicyRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        call.return_value = policy.Policy()

        client.set_iam_policy(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_set_iam_policy_from_dict():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client._transport.set_iam_policy), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = policy.Policy()

        response = client.set_iam_policy(
            request={"resource": "resource_value", "policy": policy.Policy(version=774)}
        )
        call.assert_called()


def test_test_iam_permissions(transport: str = "grpc"):
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(), transport=transport
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = iam_policy.TestIamPermissionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse(
            permissions=["permissions_value"]
        )

        response = client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, iam_policy.TestIamPermissionsResponse)
    assert response.permissions == ["permissions_value"]


def test_test_iam_permissions_field_headers():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = iam_policy.TestIamPermissionsRequest()
    request.resource = "resource/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        call.return_value = iam_policy.TestIamPermissionsResponse()

        client.test_iam_permissions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "resource=resource/value") in kw["metadata"]


def test_test_iam_permissions_from_dict():
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())
    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client._transport.test_iam_permissions), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = iam_policy.TestIamPermissionsResponse()

        response = client.test_iam_permissions(
            request={"resource": "resource_value", "permissions": ["permissions_value"]}
        )
        call.assert_called()


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.RegistrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    with pytest.raises(ValueError):
        client = RegistrationServiceClient(
            credentials=credentials.AnonymousCredentials(), transport=transport
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.RegistrationServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials()
    )
    client = RegistrationServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = RegistrationServiceClient(credentials=credentials.AnonymousCredentials())
    assert isinstance(client._transport, transports.RegistrationServiceGrpcTransport)


def test_registration_service_base_transport():
    # Instantiate the base transport.
    transport = transports.RegistrationServiceTransport(
        credentials=credentials.AnonymousCredentials()
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "create_namespace",
        "list_namespaces",
        "get_namespace",
        "update_namespace",
        "delete_namespace",
        "create_service",
        "list_services",
        "get_service",
        "update_service",
        "delete_service",
        "create_endpoint",
        "list_endpoints",
        "get_endpoint",
        "update_endpoint",
        "delete_endpoint",
        "get_iam_policy",
        "set_iam_policy",
        "test_iam_permissions",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_registration_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        RegistrationServiceClient()
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_registration_service_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.RegistrationServiceGrpcTransport(host="squid.clam.whelk")
        adc.assert_called_once_with(
            scopes=("https://www.googleapis.com/auth/cloud-platform",)
        )


def test_registration_service_host_no_port():
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicedirectory.googleapis.com"
        ),
    )
    assert client._transport._host == "servicedirectory.googleapis.com:443"


def test_registration_service_host_with_port():
    client = RegistrationServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="servicedirectory.googleapis.com:8000"
        ),
    )
    assert client._transport._host == "servicedirectory.googleapis.com:8000"


def test_registration_service_grpc_transport_channel():
    channel = grpc.insecure_channel("http://localhost/")

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.RegistrationServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_registration_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.RegistrationServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=("https://www.googleapis.com/auth/cloud-platform",),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_registration_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.RegistrationServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=("https://www.googleapis.com/auth/cloud-platform",),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_service_path():
    project = "squid"
    location = "clam"
    namespace = "whelk"
    service = "octopus"

    expected = "projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}".format(
        project=project, location=location, namespace=namespace, service=service
    )
    actual = RegistrationServiceClient.service_path(
        project, location, namespace, service
    )
    assert expected == actual


def test_parse_service_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "namespace": "cuttlefish",
        "service": "mussel",
    }
    path = RegistrationServiceClient.service_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistrationServiceClient.parse_service_path(path)
    assert expected == actual


def test_endpoint_path():
    project = "squid"
    location = "clam"
    namespace = "whelk"
    service = "octopus"
    endpoint = "oyster"

    expected = "projects/{project}/locations/{location}/namespaces/{namespace}/services/{service}/endpoints/{endpoint}".format(
        project=project,
        location=location,
        namespace=namespace,
        service=service,
        endpoint=endpoint,
    )
    actual = RegistrationServiceClient.endpoint_path(
        project, location, namespace, service, endpoint
    )
    assert expected == actual


def test_parse_endpoint_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "namespace": "mussel",
        "service": "winkle",
        "endpoint": "nautilus",
    }
    path = RegistrationServiceClient.endpoint_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistrationServiceClient.parse_endpoint_path(path)
    assert expected == actual


def test_namespace_path():
    project = "squid"
    location = "clam"
    namespace = "whelk"

    expected = "projects/{project}/locations/{location}/namespaces/{namespace}".format(
        project=project, location=location, namespace=namespace
    )
    actual = RegistrationServiceClient.namespace_path(project, location, namespace)
    assert expected == actual


def test_parse_namespace_path():
    expected = {"project": "octopus", "location": "oyster", "namespace": "nudibranch"}
    path = RegistrationServiceClient.namespace_path(**expected)

    # Check that the path construction is reversible.
    actual = RegistrationServiceClient.parse_namespace_path(path)
    assert expected == actual
