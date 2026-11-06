# HR search demo: Microsoft Foundry (Content Understanding and the two models),
# Azure AI Search, and who can use them. Everything uses Microsoft Entra ID; keys
# are turned off. The mock Workday API is in workday.tf.

data "azurerm_client_config" "current" {}

resource "random_string" "suffix" {
  length  = 5
  special = false
  upper   = false
}

locals {
  suffix = random_string.suffix.result
  tags   = { SecurityControl = "Ignore" }
  me     = data.azurerm_client_config.current.object_id
}

resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
  tags     = local.tags
}

# Content Understanding turns the PDFs into Markdown; notebook 01 also embeds the chunks here.
resource "azurerm_cognitive_account" "foundry" {
  name                  = "hr-search-foundry-${local.suffix}"
  resource_group_name   = azurerm_resource_group.main.name
  location              = azurerm_resource_group.main.location
  kind                  = "AIServices"
  sku_name              = "S0"
  custom_subdomain_name = "hr-search-foundry-${local.suffix}"
  local_auth_enabled    = false
  tags                  = local.tags
}

# The newest, largest model Content Understanding supports.
resource "azurerm_cognitive_deployment" "completion" {
  name                 = "gpt-5.5"
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  model {
    format  = "OpenAI"
    name    = "gpt-5.5"
    version = "2026-04-24"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 200
  }
}

resource "azurerm_cognitive_deployment" "embedding" {
  name                 = "text-embedding-3-large"
  cognitive_account_id = azurerm_cognitive_account.foundry.id

  model {
    format  = "OpenAI"
    name    = "text-embedding-3-large"
    version = "1"
  }

  sku {
    name     = "GlobalStandard"
    capacity = 200
  }

  # The account takes one deployment change at a time.
  depends_on = [azurerm_cognitive_deployment.completion]
}

resource "azurerm_search_service" "search" {
  name                         = "hr-search-${local.suffix}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  sku                          = "basic"
  semantic_search_sku          = "free"
  local_authentication_enabled = false
  tags                         = local.tags

  # Vectorizes queries with the embedding model as itself.
  identity {
    type = "SystemAssigned"
  }
}

locals {
  role_assignments = {
    # You build, fill and query the index.
    me-search-service = { scope = azurerm_search_service.search.id, role = "Search Service Contributor", principal = local.me, type = null }
    me-search-data    = { scope = azurerm_search_service.search.id, role = "Search Index Data Contributor", principal = local.me, type = null }
    me-foundry        = { scope = azurerm_cognitive_account.foundry.id, role = "Cognitive Services User", principal = local.me, type = null }
    # Terraform seeds the worker table, and `func start` reads it, as you.
    me-workers = { scope = azurerm_storage_account.workday.id, role = "Storage Table Data Contributor", principal = local.me, type = null }

    search-embeddings = { scope = azurerm_cognitive_account.foundry.id, role = "Cognitive Services OpenAI User", principal = azurerm_search_service.search.identity[0].principal_id, type = "ServicePrincipal" }
    copilot-search    = { scope = azurerm_search_service.search.id, role = "Search Index Data Reader", principal = azuread_service_principal.search_connection.object_id, type = "ServicePrincipal" }
    workday-storage   = { scope = azurerm_storage_account.workday.id, role = "Storage Blob Data Owner", principal = azurerm_function_app_flex_consumption.workday.identity[0].principal_id, type = "ServicePrincipal" }
    workday-workers   = { scope = azurerm_storage_account.workday.id, role = "Storage Table Data Contributor", principal = azurerm_function_app_flex_consumption.workday.identity[0].principal_id, type = "ServicePrincipal" }
  }
}

resource "azurerm_role_assignment" "roles" {
  for_each             = local.role_assignments
  scope                = each.value.scope
  role_definition_name = each.value.role
  principal_id         = each.value.principal
  principal_type       = each.value.type
}
