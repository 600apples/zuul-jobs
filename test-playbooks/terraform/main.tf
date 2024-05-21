resource "local_file" "test_file" {
  content = "test-content"
  filename = "${path.module}/test-file"
}

module "test_module" {
  source = "git::https://example.org/this/module/does/not/exist.git//module"
}
