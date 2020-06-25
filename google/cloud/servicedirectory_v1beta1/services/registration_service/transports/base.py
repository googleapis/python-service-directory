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

import abc
import typing

from google import auth
from google.auth import credentials  # type: ignore

from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service
from google.cloud.servicedirectory_v1beta1.types import service as gcs_service
from google.iam.v1 import iam_policy_pb2 as iam_policy  # type: ignore
from google.iam.v1 import policy_pb2 as policy  # type: ignore
from google.protobuf import empty_pb2 as empty  # type: ignore


class RegistrationServiceTransport(abc.ABC):
    """Abstract transport class for RegistrationService."""

    AUTH_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        *,
        host: str = "servicedirectory.googleapis.com",
        credentials: credentials.Credentials = None,
        **kwargs,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
        """
        # Save the hostname. Default to port 443 (HTTPS) if none is specified.
        if ":" not in host:
            host += ":443"
        self._host = host

        # If no credentials are provided, then determine the appropriate
        # defaults.
        if credentials is None:
            credentials, _ = auth.default(scopes=self.AUTH_SCOPES)

        # Save the credentials.
        self._credentials = credentials

    @property
    def create_namespace(
        self
    ) -> typing.Callable[
        [registration_service.CreateNamespaceRequest],
        typing.Union[
            gcs_namespace.Namespace, typing.Awaitable[gcs_namespace.Namespace]
        ],
    ]:
        raise NotImplementedError()

    @property
    def list_namespaces(
        self
    ) -> typing.Callable[
        [registration_service.ListNamespacesRequest],
        typing.Union[
            registration_service.ListNamespacesResponse,
            typing.Awaitable[registration_service.ListNamespacesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_namespace(
        self
    ) -> typing.Callable[
        [registration_service.GetNamespaceRequest],
        typing.Union[namespace.Namespace, typing.Awaitable[namespace.Namespace]],
    ]:
        raise NotImplementedError()

    @property
    def update_namespace(
        self
    ) -> typing.Callable[
        [registration_service.UpdateNamespaceRequest],
        typing.Union[
            gcs_namespace.Namespace, typing.Awaitable[gcs_namespace.Namespace]
        ],
    ]:
        raise NotImplementedError()

    @property
    def delete_namespace(
        self
    ) -> typing.Callable[
        [registration_service.DeleteNamespaceRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_service(
        self
    ) -> typing.Callable[
        [registration_service.CreateServiceRequest],
        typing.Union[gcs_service.Service, typing.Awaitable[gcs_service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def list_services(
        self
    ) -> typing.Callable[
        [registration_service.ListServicesRequest],
        typing.Union[
            registration_service.ListServicesResponse,
            typing.Awaitable[registration_service.ListServicesResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_service(
        self
    ) -> typing.Callable[
        [registration_service.GetServiceRequest],
        typing.Union[service.Service, typing.Awaitable[service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def update_service(
        self
    ) -> typing.Callable[
        [registration_service.UpdateServiceRequest],
        typing.Union[gcs_service.Service, typing.Awaitable[gcs_service.Service]],
    ]:
        raise NotImplementedError()

    @property
    def delete_service(
        self
    ) -> typing.Callable[
        [registration_service.DeleteServiceRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def create_endpoint(
        self
    ) -> typing.Callable[
        [registration_service.CreateEndpointRequest],
        typing.Union[gcs_endpoint.Endpoint, typing.Awaitable[gcs_endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def list_endpoints(
        self
    ) -> typing.Callable[
        [registration_service.ListEndpointsRequest],
        typing.Union[
            registration_service.ListEndpointsResponse,
            typing.Awaitable[registration_service.ListEndpointsResponse],
        ],
    ]:
        raise NotImplementedError()

    @property
    def get_endpoint(
        self
    ) -> typing.Callable[
        [registration_service.GetEndpointRequest],
        typing.Union[endpoint.Endpoint, typing.Awaitable[endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def update_endpoint(
        self
    ) -> typing.Callable[
        [registration_service.UpdateEndpointRequest],
        typing.Union[gcs_endpoint.Endpoint, typing.Awaitable[gcs_endpoint.Endpoint]],
    ]:
        raise NotImplementedError()

    @property
    def delete_endpoint(
        self
    ) -> typing.Callable[
        [registration_service.DeleteEndpointRequest],
        typing.Union[empty.Empty, typing.Awaitable[empty.Empty]],
    ]:
        raise NotImplementedError()

    @property
    def get_iam_policy(
        self
    ) -> typing.Callable[
        [iam_policy.GetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def set_iam_policy(
        self
    ) -> typing.Callable[
        [iam_policy.SetIamPolicyRequest],
        typing.Union[policy.Policy, typing.Awaitable[policy.Policy]],
    ]:
        raise NotImplementedError()

    @property
    def test_iam_permissions(
        self
    ) -> typing.Callable[
        [iam_policy.TestIamPermissionsRequest],
        typing.Union[
            iam_policy.TestIamPermissionsResponse,
            typing.Awaitable[iam_policy.TestIamPermissionsResponse],
        ],
    ]:
        raise NotImplementedError()


__all__ = ("RegistrationServiceTransport",)
