import subprocess
import json

def main():
    permissions_to_check = ["iam:CreateServiceLinkedRole", "iam:SimulatePrincipalPolicy", "iam:TagRole",
                            "ec2:DescribeLaunchTemplateVersions", "ec2:DescribeLaunchTemplates", 
                            "ec2:DescribeNatGateways", "ec2:DescribeAddresses", "ec2:DescribeSubnets", 
                            "ec2:DescribeAccountAttributes", "ec2:DescribeAvailabilityZones", 
                            "ec2:DescribeRouteTables", "ec2:DescribeSecurityGroups", "ec2:DescribeVpcs", 
                            "ec2:DescribeInternetGateways", "ec2:CreateTags", "iam:PassRole", "ec2:DescribeImages", 
                            "lambda:InvokeFunction", "lambda:CreateFunction", "iam:GetPolicyVersion", 
                            "ec2:AuthorizeSecurityGroupIngress", "ec2:DeleteSubnet", "ec2:CreateKeyPair", 
                            "iam:RemoveRoleFromInstanceProfile", "iam:CreateRole", "ec2:AttachInternetGateway", 
                            "iam:AttachRolePolicy", "iam:AddRoleToInstanceProfile", "ec2:DeleteRouteTable", 
                            "ec2:AssociateRouteTable", "ssm:DeleteParameter", "cloudformation:DescribeStackEvents", 
                            "iam:DetachRolePolicy", "autoscaling:DescribeAutoScalingGroups", "ec2:CreateRoute", 
                            "ec2:CreateInternetGateway", "iam:ListAttachedRolePolicies", 
                            "autoscaling:UpdateAutoScalingGroup", "ec2:DeleteInternetGateway", "lambda:DeleteFunction",
                            "iam:ListRolePolicies", "cloudformation:ListStackResources", "iam:ListPolicies", 
                            "iam:GetRole", "iam:GetPolicy", "ec2:CreateRouteTable", "ec2:RunInstances", 
                            "iam:DeleteRole", "ec2:DetachInternetGateway", "ssm:GetParameters", 
                            "ec2:DisassociateRouteTable", "lambda:GetFunctionCodeSigningConfig", 
                            "cloudformation:DescribeStacks", "ssm:PutParameter", "cloudformation:DeleteStack", 
                            "ec2:DeleteNatGateway", "ec2:DeleteVpc", "ec2:CreateSubnet", 
                            "autoscaling:CreateAutoScalingGroup", "ec2:DeleteKeyPair", "iam:GetAccountSummary", 
                            "iam:CreateInstanceProfile", "ec2:CreateNatGateway", "ec2:DescribeRegions", 
                            "ec2:CreateVpc", "ec2:ModifySubnetAttribute", "autoscaling:DescribeScalingActivities", 
                            "ec2:CreateSecurityGroup", "lambda:GetRuntimeManagementConfig", "ec2:ModifyVpcAttribute", 
                            "ec2:ReleaseAddress", "iam:DeleteInstanceProfile", "ec2:DeleteLaunchTemplate", 
                            "cloudformation:ListStacks", "iam:GetInstanceProfile", "lambda:GetFunction", 
                            "ec2:DeleteRoute", "iam:ListRoles", "cloudformation:GetTemplateSummary", 
                            "ec2:AllocateAddress", "iam:CreatePolicy", "ec2:CreateLaunchTemplate", 
                            "iam:ListPolicyVersions", "cloudformation:CreateStack", "ec2:DeleteSecurityGroup"]
    result = subprocess.check_output(['aws', 'sts', 'get-caller-identity'])

    user_arn = json.loads(result)['Arn']

    # Simulate the IAM policy to check permissions
    result = subprocess.check_output(['aws', 'iam', 'simulate-principal-policy',
                                      '--policy-source-arn', user_arn,
                                      '--action-names'] + permissions_to_check)

    # Parse the result and check for allowed and denied permissions
    result_json = json.loads(result)
    allowed_permissions = result_json.get('EvaluationResults', [])
    
    for permission in permissions_to_check:
        is_allowed = any(p.get('EvalActionName') == permission and p.get('EvalDecision') == 'allowed' for p in allowed_permissions)
        print(f"{permission}: {'Allowed' if is_allowed else 'Denied'}")

if __name__ == '__main__':
    main()
