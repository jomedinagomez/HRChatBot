variable "subscription_id" {
  description = "Azure subscription to deploy to."
  type        = string
}

variable "location" {
  description = "Azure region for every resource."
  type        = string
  default     = "westus3"
}

variable "resource_group_name" {
  description = "Resource group that holds everything."
  type        = string
  default     = "rg-hr-search-demo"
}

variable "power_platform_environment_url" {
  description = "Power Platform environment for the Copilot Studio agent (https://<org>.crm.dynamics.com). Only written to .env for notebook 04."
  type        = string
  default     = ""
}
