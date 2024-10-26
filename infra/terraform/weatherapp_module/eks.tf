provider "aws" {
  region = var.region
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "eks_cluster" {
  name        = "${var.cluster_name}-cluster-sg"
  description = "Security group for EKS cluster"
  vpc_id      = data.aws_vpc.default.id

  # CoreDNS TCP
  ingress {
    description = "Allow CoreDNS TCP"
    from_port   = 53
    to_port     = 53
    protocol    = "tcp"
    self        = true
  }

  # CoreDNS UDP
  ingress {
    description = "Allow CoreDNS UDP"
    from_port   = 53
    to_port     = 53
    protocol    = "udp"
    self        = true
  }

  # metrics server
  ingress {
    description = "Allow metrics server"
    from_port   = 4443
    to_port     = 4443
    protocol    = "tcp"
    self        = true
  }

  ingress {
    description = "Allow coredns 443"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    self        = true
  }

  # kubelet communication
  ingress {
    description = "Allow kubelet communication"
    from_port   = 10250
    to_port     = 10250
    protocol    = "tcp"
    self        = true
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.cluster_name}-cluster-sg"
  }
}

resource "aws_eks_cluster" "cluster" {
  name     = var.cluster_name
  version  = var.cluster_version
  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {
    subnet_ids = data.aws_subnets.default_subnets.ids
    security_group_ids = [aws_security_group.eks_cluster.id]
  }

  depends_on = [
    aws_security_group.eks_cluster
  ]

}

resource "aws_eks_addon" "vpc_cni" {
  cluster_name = aws_eks_cluster.cluster.name
  addon_name   = "vpc-cni"
  resolve_conflicts = "OVERWRITE"
}

resource "aws_eks_addon" "coredns" {
  cluster_name = aws_eks_cluster.cluster.name
  addon_name   = "coredns"
  resolve_conflicts = "OVERWRITE"
}

resource "aws_eks_addon" "kube_proxy" {
  cluster_name = aws_eks_cluster.cluster.name
  addon_name   = "kube-proxy"
  resolve_conflicts = "OVERWRITE"
}
