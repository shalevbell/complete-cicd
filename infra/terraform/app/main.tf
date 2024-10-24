terraform {
  backend "s3" {
    bucket = "shalev-tf"
    key    = "tfstate/weatherapp.tfstate"
    region = "eu-central-1"
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}

module "app" {
  source          = "../weatherapp_module"
  region          = var.region
  cluster_name    = var.cluster_name
  desired_size    = var.desired_size
  max_size        = var.max_size
  min_size        = var.min_size
  cluster_version = var.cluster_version
}
