locals {
  workday_mock_url = "https://${azurerm_function_app_flex_consumption.workday.default_hostname}/api/workers/me"
}

output "search_endpoint" {
  value = "https://${azurerm_search_service.search.name}.search.windows.net"
}

output "foundry_endpoint" {
  value = "https://${azurerm_cognitive_account.foundry.custom_subdomain_name}.services.ai.azure.com/"
}

output "workday_mock_url" {
  value = local.workday_mock_url
}

output "workday_function_app" {
  value = azurerm_function_app_flex_consumption.workday.name
}

output "workday_api_app_id" {
  value = azuread_application_registration.workday_api.client_id
}

output "workday_connector_app_id" {
  value = azuread_application_registration.workday_connector.client_id
}

output "workday_connector_client_secret" {
  value     = azuread_application_password.workday_connector.value
  sensitive = true
}

output "search_connection_client_secret" {
  value     = azuread_application_password.search_connection.value
  sensitive = true
}

output "portal_url" {
  value = "https://portal.azure.com/#@${data.azurerm_client_config.current.tenant_id}/resource${azurerm_resource_group.main.id}"
}

# The notebooks and scripts read .env; Terraform rewrites it with what it deployed.
resource "local_file" "dotenv" {
  filename = "${path.module}/../.env"
  content  = <<-EOT
    # Written by terraform apply (infra/). Rerun it rather than editing this file.
    AZURE_SUBSCRIPTION_ID=${var.subscription_id}
    AZURE_TENANT_ID=${data.azurerm_client_config.current.tenant_id}
    CONTENTUNDERSTANDING_ENDPOINT=https://${azurerm_cognitive_account.foundry.custom_subdomain_name}.services.ai.azure.com/
    AZURE_OPENAI_ENDPOINT=https://${azurerm_cognitive_account.foundry.custom_subdomain_name}.openai.azure.com/
    AZURE_OPENAI_API_VERSION=2024-10-21
    EXTRACTION_DEPLOYMENT=${azurerm_cognitive_deployment.completion.name}
    EMBEDDING_DEPLOYMENT=${azurerm_cognitive_deployment.embedding.name}
    SEARCH_ENDPOINT=https://${azurerm_search_service.search.name}.search.windows.net
    SEARCH_INDEX=hr-demo
    WORKDAY_MOCK_URL=${local.workday_mock_url}
    WORKDAY_API_APP_ID=${azuread_application_registration.workday_api.client_id}
    WORKDAY_CONNECTOR_APP_ID=${azuread_application_registration.workday_connector.client_id}
    POWER_PLATFORM_ENVIRONMENT=${var.power_platform_environment_url}
    SEARCH_CONNECTION_APP_ID=${azuread_application_registration.search_connection.client_id}
  EOT
}

# Points `func start` at the same worker table, read with your az login.
resource "local_file" "workday_local_settings" {
  filename = "${path.module}/../mock_workday/local.settings.json"
  content = jsonencode({
    IsEncrypted = false
    Values = {
      FUNCTIONS_WORKER_RUNTIME    = "python"
      AzureWebJobsStorage         = ""
      AZURE_FUNCTIONS_ENVIRONMENT = "Development"
      WORKERS_TABLE_ENDPOINT      = azurerm_storage_account.workday.primary_table_endpoint
    }
  })
}
