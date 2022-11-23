import sys

from client import KuFlowClient

def main() -> int:
    """Echo the input arguments to standard output"""

    client = KuFlowClient(
        username="1e96158f-3dfd-4c4c-8aa2-4c61a7127bcf",
        password="*pn8BMkt-KI0/08",
        endpoint="http://localhost:8080/apis/external/v2022-10-08",
        allow_insecure_connection=True
    )
    principals = client.principals.find_principals(
        group_id='c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f'
    )
    print(principals)

    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
