terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "ghostos_api" {
  name         = "ghostos-api:latest"
  keep_locally = false
}

resource "docker_container" "ghostos_api_container" {
  image = docker_image.ghostos_api.image_id
  name  = "ghostos-api-prod"
  ports {
    internal = 8000
    external = 8008 # Map to a different external port
  }
}
