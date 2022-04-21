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

__protobuf__ = proto.module(
    package="google.cloud.servicedirectory.v1",
    manifest={
        "Namespace",
    },
)


class Namespace(proto.Message):
    r"""A container for
    [services][google.cloud.servicedirectory.v1.Service]. Namespaces
    allow administrators to group services together and define
    permissions for a collection of services.

    Attributes:
        name (str):
            Immutable. The resource name for the namespace in the format
            ``projects/*/locations/*/namespaces/*``.
        labels (Mapping[str, str]):
            Optional. Resource labels associated with
            this Namespace. No more than 64 user labels can
            be associated with a given resource.  Label keys
            and values can be no longer than 63 characters.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    labels = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
