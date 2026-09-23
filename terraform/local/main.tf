terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

resource "local_file" "lab_note" {
  filename = "${path.module}/lab-note.txt"
  content  = "My incident response lab is managed with Terraform.\n"
}