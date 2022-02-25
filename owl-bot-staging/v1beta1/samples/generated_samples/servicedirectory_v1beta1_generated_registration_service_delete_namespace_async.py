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
# Generated code. DO NOT EDIT!
#
# Snippet for DeleteNamespace
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-service-directory


# [START servicedirectory_v1beta1_generated_RegistrationService_DeleteNamespace_async]
from google.cloud import servicedirectory_v1beta1


async def sample_delete_namespace():
    # Create a client
    client = servicedirectory_v1beta1.RegistrationServiceAsyncClient()

    # Initialize request argument(s)
    request = servicedirectory_v1beta1.DeleteNamespaceRequest(
        name="name_value",
    )

    # Make the request
    await client.delete_namespace(request=request)


# [END servicedirectory_v1beta1_generated_RegistrationService_DeleteNamespace_async]