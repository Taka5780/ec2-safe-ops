locals {
  test_instances = {
    "dev-running" = { env = "dev", state = "running" }        # Expected value: STOP
    "stg-stopped" = { env = "stg", state = "stopped" }        # Expected value: DELETE
    "prod-locked" = { env = "prod", state = "running" }       # Expected value: SKIP (Production Defense)
    "prd-old"     = { env = "production", state = "stopped" } # Expected value: SKIP (Production Defense)
    "no-tag-user" = { env = "", state = "running" }           # Expected value: SKIP (Unmarked Defense)
  }
}

resource "aws_instance" "sandbox" {
  for_each      = local.test_instances
  ami           = "ami-088b486f20fab3f0e"
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id

  tags = {
    Name = "Sandbox-${each.key}"
    Env  = each.value.env
  }
}

resource "aws_ec2_instance_state" "sandbox_state" {
  for_each    = local.test_instances
  instance_id = aws_instance.sandbox[each.key].id
  state       = each.value.state
}
