"""Mock Workday: returns the caller's own worker record.

As with Workday's delegated OAuth, the caller is whoever their Microsoft Entra token
says they are. In Azure, App Service authentication validates the token before the
function runs and passes its claims along; there are no keys. Records use the field
names of Workday's worker summary (isManager, primaryWorkEmail, ...) and live in a
storage table, read with the function's own identity (your az login when run locally),
so a role can change on the fly.
"""

import base64
import json
import os

import azure.functions as func
from azure.data.tables import TableClient, UpdateMode
from azure.identity import DefaultAzureCredential

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
workers = TableClient(os.environ["WORKERS_TABLE_ENDPOINT"], "workers", credential=DefaultAzureCredential())
RUNNING_LOCALLY = os.environ.get("AZURE_FUNCTIONS_ENVIRONMENT") == "Development"


def caller_claims(req):
    principal = req.headers.get("X-MS-CLIENT-PRINCIPAL")
    if principal:
        claims = {}
        for claim in json.loads(base64.b64decode(principal))["claims"]:
            claims.setdefault(claim["typ"].rsplit("/", 1)[-1], []).append(claim["val"])
        return claims
    # `func start` has no App Service authentication, so locally the token is read
    # without being validated. In Azure this branch never runs.
    token = req.headers.get("Authorization", "").removeprefix("Bearer ")
    if RUNNING_LOCALLY and token.count(".") == 2:
        payload = token.split(".")[1]
        decoded = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
        return {name: value if isinstance(value, list) else [value] for name, value in decoded.items()}
    return {}


def caller(claims):
    # A user's principal name, or a service principal's client ID.
    return (claims.get("upn") or claims.get("unique_name") or claims.get("appid") or [""])[0].lower()


def find_worker(user):
    rows = workers.query_entities("PartitionKey eq 'workers' and RowKey eq @user", parameters={"user": user})
    row = next(iter(rows), None)
    return json.loads(row["worker"]) if row else None


@app.route(route="workers/me", methods=["GET"])
def get_my_worker(req: func.HttpRequest) -> func.HttpResponse:
    user = caller(caller_claims(req))
    worker = find_worker(user)
    if worker is None:
        return func.HttpResponse(json.dumps({"error": "Worker not found", "caller": user}), status_code=404, mimetype="application/json")
    return func.HttpResponse(json.dumps(worker), mimetype="application/json")


# Mock only: add a worker or change a field such as isManager. Needs the
# Workers.Admin app role, which the agent's users don't have.
@app.route(route="workers/{user}", methods=["PUT"])
def put_worker(req: func.HttpRequest) -> func.HttpResponse:
    claims = caller_claims(req)
    if "Workers.Admin" not in claims.get("roles", []) + claims.get("role", []):
        return func.HttpResponse('{"error": "Needs the Workers.Admin role"}', status_code=403, mimetype="application/json")
    user = req.route_params["user"].strip().lower()
    worker = find_worker(user) or {"descriptor": user, "primaryWorkEmail": user, "isManager": False}
    worker.update(req.get_json())
    workers.upsert_entity({"PartitionKey": "workers", "RowKey": user, "worker": json.dumps(worker)}, mode=UpdateMode.REPLACE)
    return func.HttpResponse(json.dumps(worker), mimetype="application/json")
