# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
import proto  # type: ignore

from google.cloud.servicedirectory_v1.types import endpoint as gcs_endpoint
from google.cloud.servicedirectory_v1.types import namespace as gcs_namespace
from google.cloud.servicedirectory_v1.types import service as gcs_service
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.servicedirectory.v1",
    manifest={
        "CreateNamespaceRequest",
        "ListNamespacesRequest",
        "ListNamespacesResponse",
        "GetNamespaceRequest",
        "UpdateNamespaceRequest",
        "DeleteNamespaceRequest",
        "CreateServiceRequest",
        "ListServicesRequest",
        "ListServicesResponse",
        "GetServiceRequest",
        "UpdateServiceRequest",
        "DeleteServiceRequest",
        "CreateEndpointRequest",
        "ListEndpointsRequest",
        "ListEndpointsResponse",
        "GetEndpointRequest",
        "UpdateEndpointRequest",
        "DeleteEndpointRequest",
    },
)


class CreateNamespaceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.CreateNamespace][google.cloud.servicedirectory.v1.RegistrationService.CreateNamespace].

    Attributes:
        parent (str):
            Required. The resource name of the project
            and location the namespace will be created in.
        namespace_id (str):
            Required. The Resource ID must be 1-63 characters long, and
            comply with RFC1035. Specifically, the name must be 1-63
            characters long and match the regular expression
            ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the first
            character must be a lowercase letter, and all following
            characters must be a dash, lowercase letter, or digit,
            except the last character, which cannot be a dash.
        namespace (google.cloud.servicedirectory_v1.types.Namespace):
            Required. A namespace with initial fields
            set.
    """

    parent = proto.Field(proto.STRING, number=1,)
    namespace_id = proto.Field(proto.STRING, number=2,)
    namespace = proto.Field(proto.MESSAGE, number=3, message=gcs_namespace.Namespace,)


class ListNamespacesRequest(proto.Message):
    r"""The request message for
    [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1.RegistrationService.ListNamespaces].

    Attributes:
        parent (str):
            Required. The resource name of the project
            and location whose namespaces we'd like to list.
        page_size (int):
            Optional. The maximum number of items to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
        filter (str):
            Optional. The filter to list result by.

            General filter string syntax: () can be "name", or "labels."
            for map field. can be "<, >, <=, >=, !=, =, :". Of which ":"
            means HAS, and is roughly the same as "=". must be the same
            data type as field. can be "AND, OR, NOT".

            Examples of valid filters:

            -  "labels.owner" returns Namespaces that have a label with
               the key "owner" this is the same as "labels:owner".
            -  "labels.protocol=gRPC" returns Namespaces that have
               key/value "protocol=gRPC".
            -  "name>projects/my-project/locations/us-east/namespaces/namespace-c"
               returns Namespaces that have name that is alphabetically
               later than the string, so "namespace-e" will be returned
               but "namespace-a" will not be.
            -  "labels.owner!=sd AND labels.foo=bar" returns Namespaces
               that have "owner" in label key but value is not "sd" AND
               have key/value foo=bar.
            -  "doesnotexist.foo=bar" returns an empty list. Note that
               Namespace doesn't have a field called "doesnotexist".
               Since the filter does not match any Namespaces, it
               returns no results.
        order_by (str):
            Optional. The order to list result by.

            General order by string syntax: (<asc|desc>) (,) allows
            values {"name"} <asc/desc> ascending or descending order by
            . If this is left blank, "asc" is used. Note that an empty
            order_by string result in default order, which is order by
            name in ascending order.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListNamespacesResponse(proto.Message):
    r"""The response message for
    [RegistrationService.ListNamespaces][google.cloud.servicedirectory.v1.RegistrationService.ListNamespaces].

    Attributes:
        namespaces (Sequence[google.cloud.servicedirectory_v1.types.Namespace]):
            The list of namespaces.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    namespaces = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gcs_namespace.Namespace,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetNamespaceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.GetNamespace][google.cloud.servicedirectory.v1.RegistrationService.GetNamespace].

    Attributes:
        name (str):
            Required. The name of the namespace to
            retrieve.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateNamespaceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.UpdateNamespace][google.cloud.servicedirectory.v1.RegistrationService.UpdateNamespace].

    Attributes:
        namespace (google.cloud.servicedirectory_v1.types.Namespace):
            Required. The updated namespace.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    namespace = proto.Field(proto.MESSAGE, number=1, message=gcs_namespace.Namespace,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteNamespaceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.DeleteNamespace][google.cloud.servicedirectory.v1.RegistrationService.DeleteNamespace].

    Attributes:
        name (str):
            Required. The name of the namespace to
            delete.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateServiceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.CreateService][google.cloud.servicedirectory.v1.RegistrationService.CreateService].

    Attributes:
        parent (str):
            Required. The resource name of the namespace
            this service will belong to.
        service_id (str):
            Required. The Resource ID must be 1-63 characters long, and
            comply with RFC1035. Specifically, the name must be 1-63
            characters long and match the regular expression
            ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the first
            character must be a lowercase letter, and all following
            characters must be a dash, lowercase letter, or digit,
            except the last character, which cannot be a dash.
        service (google.cloud.servicedirectory_v1.types.Service):
            Required. A service  with initial fields set.
    """

    parent = proto.Field(proto.STRING, number=1,)
    service_id = proto.Field(proto.STRING, number=2,)
    service = proto.Field(proto.MESSAGE, number=3, message=gcs_service.Service,)


class ListServicesRequest(proto.Message):
    r"""The request message for
    [RegistrationService.ListServices][google.cloud.servicedirectory.v1.RegistrationService.ListServices].

    Attributes:
        parent (str):
            Required. The resource name of the namespace
            whose services we'd like to list.
        page_size (int):
            Optional. The maximum number of items to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
        filter (str):
            Optional. The filter to list result by.

            General filter string syntax: () can be "name", or
            "metadata." for map field. can be "<, >, <=, >=, !=, =, :".
            Of which ":" means HAS, and is roughly the same as "=". must
            be the same data type as field. can be "AND, OR, NOT".

            Examples of valid filters:

            -  "metadata.owner" returns Services that have a label with
               the key "owner" this is the same as "metadata:owner".
            -  "metadata.protocol=gRPC" returns Services that have
               key/value "protocol=gRPC".
            -  "name>projects/my-project/locations/us-east/namespaces/my-namespace/services/service-c"
               returns Services that have name that is alphabetically
               later than the string, so "service-e" will be returned
               but "service-a" will not be.
            -  "metadata.owner!=sd AND metadata.foo=bar" returns
               Services that have "owner" in label key but value is not
               "sd" AND have key/value foo=bar.
            -  "doesnotexist.foo=bar" returns an empty list. Note that
               Service doesn't have a field called "doesnotexist". Since
               the filter does not match any Services, it returns no
               results.
        order_by (str):
            Optional. The order to list result by.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListServicesResponse(proto.Message):
    r"""The response message for
    [RegistrationService.ListServices][google.cloud.servicedirectory.v1.RegistrationService.ListServices].

    Attributes:
        services (Sequence[google.cloud.servicedirectory_v1.types.Service]):
            The list of services.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    services = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gcs_service.Service,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetServiceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.GetService][google.cloud.servicedirectory.v1.RegistrationService.GetService].
    This should not be used for looking up a service. Insead, use the
    ``resolve`` method as it will contain all endpoints and associated
    metadata.

    Attributes:
        name (str):
            Required. The name of the service to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateServiceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.UpdateService][google.cloud.servicedirectory.v1.RegistrationService.UpdateService].

    Attributes:
        service (google.cloud.servicedirectory_v1.types.Service):
            Required. The updated service.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    service = proto.Field(proto.MESSAGE, number=1, message=gcs_service.Service,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteServiceRequest(proto.Message):
    r"""The request message for
    [RegistrationService.DeleteService][google.cloud.servicedirectory.v1.RegistrationService.DeleteService].

    Attributes:
        name (str):
            Required. The name of the service to delete.
    """

    name = proto.Field(proto.STRING, number=1,)


class CreateEndpointRequest(proto.Message):
    r"""The request message for
    [RegistrationService.CreateEndpoint][google.cloud.servicedirectory.v1.RegistrationService.CreateEndpoint].

    Attributes:
        parent (str):
            Required. The resource name of the service
            that this endpoint provides.
        endpoint_id (str):
            Required. The Resource ID must be 1-63 characters long, and
            comply with RFC1035. Specifically, the name must be 1-63
            characters long and match the regular expression
            ``[a-z](?:[-a-z0-9]{0,61}[a-z0-9])?`` which means the first
            character must be a lowercase letter, and all following
            characters must be a dash, lowercase letter, or digit,
            except the last character, which cannot be a dash.
        endpoint (google.cloud.servicedirectory_v1.types.Endpoint):
            Required. A endpoint with initial fields set.
    """

    parent = proto.Field(proto.STRING, number=1,)
    endpoint_id = proto.Field(proto.STRING, number=2,)
    endpoint = proto.Field(proto.MESSAGE, number=3, message=gcs_endpoint.Endpoint,)


class ListEndpointsRequest(proto.Message):
    r"""The request message for
    [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1.RegistrationService.ListEndpoints].

    Attributes:
        parent (str):
            Required. The resource name of the service
            whose endpoints we'd like to list.
        page_size (int):
            Optional. The maximum number of items to
            return.
        page_token (str):
            Optional. The next_page_token value returned from a previous
            List request, if any.
        filter (str):
            Optional. The filter to list result by.

            General filter string syntax: () can be "name", "address",
            "port" or "metadata." for map field. can be "<, >, <=, >=,
            !=, =, :". Of which ":" means HAS, and is roughly the same
            as "=". must be the same data type as field. can be "AND,
            OR, NOT".

            Examples of valid filters:

            -  "metadata.owner" returns Endpoints that have a label with
               the key "owner" this is the same as "metadata:owner".
            -  "metadata.protocol=gRPC" returns Endpoints that have
               key/value "protocol=gRPC".
            -  "address=192.108.1.105" returns Endpoints that have this
               address.
            -  "port>8080" returns Endpoints that have port number
               larger than 8080.
            -  "name>projects/my-project/locations/us-east/namespaces/my-namespace/services/my-service/endpoints/endpoint-c"
               returns Endpoints that have name that is alphabetically
               later than the string, so "endpoint-e" will be returned
               but "endpoint-a" will not be.
            -  "metadata.owner!=sd AND metadata.foo=bar" returns
               Endpoints that have "owner" in label key but value is not
               "sd" AND have key/value foo=bar.
            -  "doesnotexist.foo=bar" returns an empty list. Note that
               Endpoint doesn't have a field called "doesnotexist".
               Since the filter does not match any Endpoints, it returns
               no results.
        order_by (str):
            Optional. The order to list result by.
    """

    parent = proto.Field(proto.STRING, number=1,)
    page_size = proto.Field(proto.INT32, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    filter = proto.Field(proto.STRING, number=4,)
    order_by = proto.Field(proto.STRING, number=5,)


class ListEndpointsResponse(proto.Message):
    r"""The response message for
    [RegistrationService.ListEndpoints][google.cloud.servicedirectory.v1.RegistrationService.ListEndpoints].

    Attributes:
        endpoints (Sequence[google.cloud.servicedirectory_v1.types.Endpoint]):
            The list of endpoints.
        next_page_token (str):
            Token to retrieve the next page of results,
            or empty if there are no more results in the
            list.
    """

    @property
    def raw_page(self):
        return self

    endpoints = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gcs_endpoint.Endpoint,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)


class GetEndpointRequest(proto.Message):
    r"""The request message for
    [RegistrationService.GetEndpoint][google.cloud.servicedirectory.v1.RegistrationService.GetEndpoint].
    This should not be used to lookup endpoints at runtime. Instead, use
    the ``resolve`` method.

    Attributes:
        name (str):
            Required. The name of the endpoint to get.
    """

    name = proto.Field(proto.STRING, number=1,)


class UpdateEndpointRequest(proto.Message):
    r"""The request message for
    [RegistrationService.UpdateEndpoint][google.cloud.servicedirectory.v1.RegistrationService.UpdateEndpoint].

    Attributes:
        endpoint (google.cloud.servicedirectory_v1.types.Endpoint):
            Required. The updated endpoint.
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Required. List of fields to be updated in
            this request.
    """

    endpoint = proto.Field(proto.MESSAGE, number=1, message=gcs_endpoint.Endpoint,)
    update_mask = proto.Field(
        proto.MESSAGE, number=2, message=field_mask_pb2.FieldMask,
    )


class DeleteEndpointRequest(proto.Message):
    r"""The request message for
    [RegistrationService.DeleteEndpoint][google.cloud.servicedirectory.v1.RegistrationService.DeleteEndpoint].

    Attributes:
        name (str):
            Required. The name of the endpoint to delete.
    """

    name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
