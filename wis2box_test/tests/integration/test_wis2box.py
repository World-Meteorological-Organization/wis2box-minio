###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# 'License'); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

# integration tests assume that the workflow in
# .github/workflows/wis2box_test.yml has been executed

import json
import os
import time
import paramiko

import requests

MINIO_SERVER_URL = 'http://localhost:4000'
WIS2BOX_API_URL = 'http://localhost:4100/oapi'
METADATA_ID = 'urn:wmo:md:universal-test:test'


def test_wis2box_data_ingest():

    # this uses the wis2box data ingest command to ingest some data
    filepath = '/data/wis2box/observations/wis2box-data-ingest_20260203.txt'
    os_command = f'docker exec minio-test-wis2box-management wis2box data ingest -p {filepath} -mdi {METADATA_ID}'
    os.system(os_command)
    # wait a bit for the data to be ingested
    time.sleep(0.5)

    # check if the data has been published
    test_url = f'{MINIO_SERVER_URL}/wis2box-public/2026-02-03/wis/{METADATA_ID}/wis2box-data-ingest_20260203.txt'
    print(test_url)
    response = requests.get(test_url)
    print(response)
    assert response.status_code == 200
    assert response.text == 'This is just some random data that will be uploaded using the wis2box data ingest command.'

def test_wis2box_sftp_upload():

    # this uses the minio client for python to upload some data to the SFTP server
    filenames = [
        'minio-SFTP_20260203.txt',
        'minio-SFTP_again_20260203.txt'
    ]
    for filename in filenames:
        filepath = f'./tests/data/observations/{filename}'
        transport = paramiko.Transport(('localhost', 4022))
        transport.connect(username='minio', password='minio123')
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(filepath, f'/wis2box-incoming/{METADATA_ID}/{filename}')
        sftp.close()
        transport.close()
        # wait a bit for the data to be ingested
        time.sleep(0.5)

        # check if the data has been published
        test_url = f'{MINIO_SERVER_URL}/wis2box-public/2026-02-03/wis/{METADATA_ID}/{filename}'
        print(test_url)
        response = requests.get(test_url)
        print(response)
        assert response.status_code == 200
        expected_text = 'This is just some random data that will be uploaded over SFTP as part of the integration tests for the wis2box-minio project.'
        assert response.text == expected_text