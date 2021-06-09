from azure.cosmos import CosmosClient, PartitionKey


def get_container(container_name):
    endpoint = "https://liteburn.documents.azure.com:443/"
    key = 'mXRGIrLXNLKF1NuATfsFlTt5Kgss9o2YQu41KUX67CwectIrxhaWoyuJVb8s8cpb1GYYKvWpFs1qVw1DEwRVFA=='

    # <create_cosmos_client>
    client = CosmosClient(endpoint, key)
    database = client.create_database_if_not_exists(id='WebStatusDatabase')
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/id"),
        offer_throughput=400
    )
    return container
