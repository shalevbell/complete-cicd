resource "aws_security_group" "eks_nodes" {
  name        = "${var.cluster_name}-nodes-sg"
  description = "Security group for EKS worker nodes"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "Allow CoreDNS TCP from cluster"
    from_port       = 53
    to_port         = 53
    protocol        = "tcp"
    security_groups = [aws_security_group.eks_cluster.id]
    self            = true
  }

  ingress {
    description     = "Allow CoreDNS UDP from cluster"
    from_port       = 53
    to_port         = 53
    protocol        = "udp"
    security_groups = [aws_security_group.eks_cluster.id]
    self            = true
  }

  ingress {
    description = "Allow inter-node communication"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self        = true
  }


  ingress {
    description     = "Allow cluster to node communication"
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.eks_cluster.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  depends_on = [
    aws_security_group.eks_cluster
  ]

  tags = {
    Name = "${var.cluster_name}-nodes-sg"
  }
}

resource "aws_launch_template" "eks_nodes" {
  name = "${var.cluster_name}-node-template"
  description = "Launch template for EKS worker nodes"

  vpc_security_group_ids = [aws_security_group.eks_nodes.id]
  
  key_name = "shalevWeatherapp"

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "${var.cluster_name}-node"
    }
  }

  depends_on = [aws_security_group.eks_nodes]
}

resource "aws_eks_node_group" "nodegroup" {
  cluster_name    = aws_eks_cluster.cluster.name
  node_group_name = "${var.cluster_name}-nodegroup"
  node_role_arn   = aws_iam_role.eks_node_group_role.arn
  subnet_ids      = data.aws_subnets.default_subnets.ids
  
  launch_template {
    id      = aws_launch_template.eks_nodes.id
    version = aws_launch_template.eks_nodes.latest_version
  }
  
  scaling_config {
    desired_size = var.desired_size
    max_size     = var.max_size
    min_size     = var.min_size
  }

  depends_on = [
    aws_launch_template.eks_nodes,
    aws_security_group.eks_nodes
  ]

  lifecycle {
    ignore_changes = [scaling_config[0].desired_size]
  }

}
