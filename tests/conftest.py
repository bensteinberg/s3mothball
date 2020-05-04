import os

import boto3
import pytest
from moto import mock_s3

from tests.helpers import write_file


@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client('s3', region_name='us-east-1')


@pytest.fixture
def source_bucket(s3):
    source_bucket = 'source'
    s3.create_bucket(Bucket=source_bucket)
    return source_bucket


@pytest.fixture
def dest_bucket(s3):
    dest_bucket = 'attic'
    s3.create_bucket(Bucket=dest_bucket)
    return dest_bucket


@pytest.fixture
def archive_url(source_bucket):
    return "s3://%s/folders/some_folder/" % source_bucket

@pytest.fixture
def tar_path(dest_bucket):
    return "s3://%s/files/folders/some_folder.tar" % dest_bucket


@pytest.fixture
def manifest_path(dest_bucket):
    return "s3://%s/manifests/folders/some_folder.tar.csv" % dest_bucket


@pytest.fixture
def files(s3, source_bucket):
    files = [
        ['folders/some_folder/file.txt', 'contents1'],
        ['folders/some_folder/file2.txt', 'contents2'],
    ]
    return [write_file(s3, source_bucket, entry[0], entry[1]) for entry in files]


