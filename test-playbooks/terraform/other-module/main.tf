resource "local_file" "test_file" {
  content = "test-content"
  filename = "${path.module}/module-test-file"
}
