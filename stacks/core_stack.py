from aws_cdk import (
    Stack,
    aws_sns as sns,
    aws_logs as logs,
    aws_iam as iam,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct

class CoreStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #1 SNS Topic for Notifications
        self.notification_topic = sns.Topic(
            self,
            "DeploymentNotifications",
            display_name="Deployment Notifications",
            topic_name="deployment-notifications",
        )

        #2 CloudWatch Log Group
        self.log_group = logs.LogGroup(
            self,
            "CoreLogGroup",
            log_group_name="/cdk/core-stack",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY
        )

        #3 IAM Roles

        #-DevOps Role
        self.devops_role = iam.Role(
            self,
            "DevOpsRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="DevOpsRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
        )

        #-ReadOnly Role
        self.read_only_role = iam.Role(
            self,
            "ReadOnlyRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="ReadOnlyRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
            ],
        )        

        self.output_arns()

        #5 Output ARNS
    
    def output_arns(self):
        CfnOutput(self, "SNSTopicARN", value=self.notification_topic.topic_arn)
        CfnOutput(self, "CloudWatchLogGroupName", value=self.log_group.log_group_name)
        CfnOutput(self, "DevOpsRoleARN", value=self.devops_role.role_arn)
        CfnOutput(self, "ReadOnlyRoleARN", value=self.read_only_role.role_arn)


        
