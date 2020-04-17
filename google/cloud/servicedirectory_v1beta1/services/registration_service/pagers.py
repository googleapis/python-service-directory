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

from typing import Any, Callable, Iterable

from google.cloud.servicedirectory_v1beta1.types import endpoint
from google.cloud.servicedirectory_v1beta1.types import namespace
from google.cloud.servicedirectory_v1beta1.types import registration_service
from google.cloud.servicedirectory_v1beta1.types import service


class ListNamespacesPager:
    """A pager for iterating through ``list_namespaces`` requests.

    This class thinly wraps an initial
    :class:`~.registration_service.ListNamespacesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``namespaces`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListNamespaces`` requests and continue to iterate
    through the ``namespaces`` field on the
    corresponding responses.

    All the usual :class:`~.registration_service.ListNamespacesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [registration_service.ListNamespacesRequest],
            registration_service.ListNamespacesResponse,
        ],
        request: registration_service.ListNamespacesRequest,
        response: registration_service.ListNamespacesResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.registration_service.ListNamespacesRequest`):
                The initial request object.
            response (:class:`~.registration_service.ListNamespacesResponse`):
                The initial response object.
        """
        self._method = method
        self._request = registration_service.ListNamespacesRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[registration_service.ListNamespacesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[namespace.Namespace]:
        for page in self.pages:
            yield from page.namespaces

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListServicesPager:
    """A pager for iterating through ``list_services`` requests.

    This class thinly wraps an initial
    :class:`~.registration_service.ListServicesResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``services`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListServices`` requests and continue to iterate
    through the ``services`` field on the
    corresponding responses.

    All the usual :class:`~.registration_service.ListServicesResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [registration_service.ListServicesRequest],
            registration_service.ListServicesResponse,
        ],
        request: registration_service.ListServicesRequest,
        response: registration_service.ListServicesResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.registration_service.ListServicesRequest`):
                The initial request object.
            response (:class:`~.registration_service.ListServicesResponse`):
                The initial response object.
        """
        self._method = method
        self._request = registration_service.ListServicesRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[registration_service.ListServicesResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[service.Service]:
        for page in self.pages:
            yield from page.services

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)


class ListEndpointsPager:
    """A pager for iterating through ``list_endpoints`` requests.

    This class thinly wraps an initial
    :class:`~.registration_service.ListEndpointsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``endpoints`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListEndpoints`` requests and continue to iterate
    through the ``endpoints`` field on the
    corresponding responses.

    All the usual :class:`~.registration_service.ListEndpointsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """

    def __init__(
        self,
        method: Callable[
            [registration_service.ListEndpointsRequest],
            registration_service.ListEndpointsResponse,
        ],
        request: registration_service.ListEndpointsRequest,
        response: registration_service.ListEndpointsResponse,
    ):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.registration_service.ListEndpointsRequest`):
                The initial request object.
            response (:class:`~.registration_service.ListEndpointsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = registration_service.ListEndpointsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[registration_service.ListEndpointsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[endpoint.Endpoint]:
        for page in self.pages:
            yield from page.endpoints

    def __repr__(self) -> str:
        return "{0}<{1!r}>".format(self.__class__.__name__, self._response)
