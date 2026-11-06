# The identity Copilot Studio's Azure AI Search connection signs in as, so the
# connection needs no one to sign in by hand: a service principal that can only read
# the index (Search Index Data Reader, in main.tf). Searches run as a service, the way
# their backend queries OpenSearch today; who sees which documents is still decided
# per user by the Workday filter. Notebook 04 creates the connection itself: the Power
# Platform Terraform provider can't, with an Azure CLI sign-in.

resource "azuread_application_registration" "search_connection" {
  display_name     = "HR Search Copilot Connection (${local.suffix})"
  sign_in_audience = "AzureADMyOrg"
}

resource "azuread_service_principal" "search_connection" {
  client_id = azuread_application_registration.search_connection.client_id
}

resource "azuread_application_password" "search_connection" {
  application_id = azuread_application_registration.search_connection.id
  display_name   = "Copilot Studio Azure AI Search connection"
}
