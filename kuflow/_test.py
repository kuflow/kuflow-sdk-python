import sys

from client import KuFlowClient, models

def main() -> int:
    """Echo the input arguments to standard output"""

    client = KuFlowClient(
        username="1e96158f-3dfd-4c4c-8aa2-4c61a7127bcf",
        password="*pn8BMkt-KI0/08",
        endpoint="http://localhost:8080/apis/external/v2022-10-08",
        allow_insecure_connection=True
    )
    principals = client.principal.find_principals(
        group_id="c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f"
    )
    print(principals)
    principals = client.principal.find_principals(
        group_id=["c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f"]
    )
    print(principals)
    principals = client.principal.find_principals(
        group_id=["c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f", "aaeb0b1d-6c3d-4436-aace-219af8a1810d"]
    )
    print(principals)

    authentication = models.Authentication(type="ENGINE")
    authentication = client.authentication.create_authentication(authentication)
    print(authentication)

    process = models.Process(
        id='28abe67f-9462-4343-b58e-c8b3344eb865',
        process_definition=models.ProcessDefinitionSummary(
            id='be35212b-deb8-4719-a10d-b8550219d156'
        )
    )
    process = client.process.create_process(process)
    print(process)

    return 0

if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
