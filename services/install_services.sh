#!/bin/bash
# Copyright (c) 2023 Cable Television Laboratories, Inc. ("CableLabs")
#                    and others.  All rights reserved.
#
# Licensed in accordance of the accompanied LICENSE.txt or LICENSE.md
# file in the base directory for this project. If none is supplied contact
# CableLabs for licensing terms of this software.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
sudo cp so_wpa_supplicant@.service /etc/systemd/system
sudo cp so_hostapd.service /etc/systemd/system
