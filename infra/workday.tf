# Mock Workday: an Azure Function behind Microsoft Entra ID that returns the caller's
# own worker record, the way the customer's Workday integration does. Two app
# registrations: one for the API, and one the Copilot Studio connector uses to call it
# on behalf of the signed-in user (OBO).

data "azuread_client_config" "current" {}

locals {
  # Pre-authorized so az and the notebooks get tokens without a consent prompt.
  azure_cli = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"
  # Azure API Connections: the Power Platform service that does the OBO token exchange.
  azure_api_connections = "fe053c5f-3692-4f14-aef2-ee34fc081cae"
  workers               = { for worker in jsondecode(file("${path.module}/../mock_workday/workers.json")) : lower(worker.primaryWorkEmail) => worker }
}

# Storage for the code package and the worker table. Shared keys are off; the function
# uses its own identity.
resource "azurerm_storage_account" "workday" {
  name                            = "hrmockwd${local.suffix}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  shared_access_key_enabled       = false
  default_to_oauth_authentication = true
  allow_nested_items_to_be_public = false
  tags                            = local.tags
}

resource "azurerm_storage_container" "deployments" {
  name                  = "deployments"
  storage_account_id    = azurerm_storage_account.workday.id
  container_access_type = "private"
}

resource "azurerm_storage_table" "workers" {
  name               = "workers"
  storage_account_id = azurerm_storage_account.workday.id
}

# New role assignments take a minute to apply.
resource "time_sleep" "storage_roles" {
  create_duration = "60s"
  depends_on      = [azurerm_role_assignment.roles]
}

# The fake employees from workers.json. Seeded once: roles changed later with
# set-role.ps1 stay as they are.
resource "azurerm_storage_table_entity" "workers" {
  for_each         = local.workers
  storage_table_id = azurerm_storage_table.workers.id
  partition_key    = "workers"
  row_key          = each.key
  entity           = { worker = jsonencode(each.value) }
  depends_on       = [time_sleep.storage_roles]

  lifecycle {
    ignore_changes = [entity]
  }
}

resource "azurerm_service_plan" "workday" {
  name                = "plan-hr-mock-workday-${local.suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "FC1"
  tags                = local.tags
}

resource "azurerm_function_app_flex_consumption" "workday" {
  name                        = "hr-mock-workday-${local.suffix}"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  service_plan_id             = azurerm_service_plan.workday.id
  storage_container_type      = "blobContainer"
  storage_container_endpoint  = "${azurerm_storage_account.workday.primary_blob_endpoint}${azurerm_storage_container.deployments.name}"
  storage_authentication_type = "SystemAssignedIdentity"
  runtime_name                = "python"
  runtime_version             = "3.12"
  maximum_instance_count      = 40
  instance_memory_in_mb       = 2048
  https_only                  = true
  tags                        = local.tags

  # Code is published with your Entra token (notebook 00), so no publishing passwords.
  webdeploy_publish_basic_authentication_enabled = false

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    AzureWebJobsStorage__accountName = azurerm_storage_account.workday.name
    WORKERS_TABLE_ENDPOINT           = azurerm_storage_account.workday.primary_table_endpoint
  }

  site_config {}

  # App Service authentication: only valid Entra tokens for the Workday API reach the code.
  auth_settings_v2 {
    auth_enabled           = true
    require_authentication = true
    unauthenticated_action = "Return401"
    require_https          = true

    active_directory_v2 {
      client_id            = azuread_application_registration.workday_api.client_id
      tenant_auth_endpoint = "https://sts.windows.net/${data.azuread_client_config.current.tenant_id}/"
      allowed_audiences    = ["api://${azuread_application_registration.workday_api.client_id}"]
      # The two callers: the Azure CLI (your az login: notebooks, set-role.ps1) and the
      # Copilot Studio connector (its OBO tokens carry the connector app's ID).
      allowed_applications = [local.azure_cli, azuread_application_registration.workday_connector.client_id]
    }

    login {
      token_store_enabled = false
    }
  }
}

# The Workday API: a delegated scope to read your own record, and an app role to
# change records (mock only).
resource "azuread_application_registration" "workday_api" {
  display_name                   = "HR Mock Workday API (${local.suffix})"
  sign_in_audience               = "AzureADMyOrg"
  requested_access_token_version = 1
}

resource "azuread_application_identifier_uri" "workday_api" {
  application_id = azuread_application_registration.workday_api.id
  identifier_uri = "api://${azuread_application_registration.workday_api.client_id}"
}

resource "random_uuid" "workers_read" {}

resource "random_uuid" "workers_admin" {}

resource "azuread_application_permission_scope" "workers_read" {
  application_id             = azuread_application_registration.workday_api.id
  scope_id                   = random_uuid.workers_read.result
  value                      = "Workers.Read"
  type                       = "User"
  admin_consent_display_name = "Read worker records"
  admin_consent_description  = "Read the signed-in user's worker record."
  user_consent_display_name  = "Read your worker record"
  user_consent_description   = "Read your own worker record."
}

resource "azuread_application_app_role" "workers_admin" {
  application_id       = azuread_application_registration.workday_api.id
  role_id              = random_uuid.workers_admin.result
  value                = "Workers.Admin"
  allowed_member_types = ["User", "Application"]
  display_name         = "Workers admin (mock only)"
  description          = "Add workers and change roles in the mock Workday."
}

resource "azuread_application_pre_authorized" "azure_cli" {
  application_id       = azuread_application_registration.workday_api.id
  authorized_client_id = local.azure_cli
  permission_ids       = [azuread_application_permission_scope.workers_read.scope_id]
}

resource "azuread_service_principal" "workday_api" {
  client_id = azuread_application_registration.workday_api.client_id
}

# You can change roles with set-role.ps1; nobody else can until given Workers.Admin too.
resource "azuread_app_role_assignment" "me_workers_admin" {
  app_role_id         = azuread_application_app_role.workers_admin.role_id
  principal_object_id = data.azuread_client_config.current.object_id
  resource_object_id  = azuread_service_principal.workday_api.object_id
}

# The connector's client app, following Microsoft's OBO setup for custom connectors:
# it asks for Workers.Read (consented for everyone) and lets Azure API Connections
# exchange the user's token. Its secret is only in Terraform state; notebook 04 hands it
# straight to the connector.
resource "azuread_application_registration" "workday_connector" {
  display_name     = "HR Mock Workday Connector (${local.suffix})"
  sign_in_audience = "AzureADMyOrg"
}

resource "azuread_application_identifier_uri" "workday_connector" {
  application_id = azuread_application_registration.workday_connector.id
  identifier_uri = "api://${azuread_application_registration.workday_connector.client_id}"
}

resource "random_uuid" "access_as_user" {}

resource "azuread_application_permission_scope" "access_as_user" {
  application_id             = azuread_application_registration.workday_connector.id
  scope_id                   = random_uuid.access_as_user.result
  value                      = "access_as_user"
  type                       = "User"
  admin_consent_display_name = "Call Workday (mock) as the signed-in user"
  admin_consent_description  = "Lets Power Platform call Workday (mock) on behalf of the signed-in user."
}

resource "azuread_application_pre_authorized" "azure_api_connections" {
  application_id       = azuread_application_registration.workday_connector.id
  authorized_client_id = local.azure_api_connections
  permission_ids       = [azuread_application_permission_scope.access_as_user.scope_id]
}

resource "azuread_application_api_access" "workday_connector" {
  application_id = azuread_application_registration.workday_connector.id
  api_client_id  = azuread_application_registration.workday_api.client_id
  scope_ids      = [azuread_application_permission_scope.workers_read.scope_id]
}

resource "azuread_service_principal" "workday_connector" {
  client_id = azuread_application_registration.workday_connector.client_id
}

resource "azuread_service_principal_delegated_permission_grant" "workday_connector" {
  service_principal_object_id          = azuread_service_principal.workday_connector.object_id
  resource_service_principal_object_id = azuread_service_principal.workday_api.object_id
  claim_values                         = [azuread_application_permission_scope.workers_read.value]
}

resource "azuread_application_password" "workday_connector" {
  application_id = azuread_application_registration.workday_connector.id
  display_name   = "Workday (mock) custom connector"
}
