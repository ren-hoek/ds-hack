from azure.storage.blob import BlockBlobService

block_blob_service = BlockBlobService(
        account_name='hmrchackathon',
        account_key='E6AiDaSVSsj7SaQWBB32KwaR4rtIAxu0+Jz8aD/V8S1jJafINMJFYDVBOic8NZVotRmKvwpGNmtT/Vh0w47zGg=='
    )
containers = block_blob_service.list_containers()
for i in containers:
    print(i.name)
    generator = block_blob_service.list_blobs(i.name)
    for blob in generator:
        print("\t Blob name: " + blob.name)
