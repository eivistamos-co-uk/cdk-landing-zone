from aws_cdk import (
    NestedStack,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_logs as logs,
    aws_iam as iam,
    aws_cloudwatch as cw,
    aws_cloudwatch_actions as cw_actions,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct

# ----------------------
# DEFINE NOTIFICATION EMAIL ADDRESS BELOW
# ----------------------

email = "eivistamos@gmail.com"

# Defining this stack as a nested stack
class CoreStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #1 Creating SNS topic for notifications
        self.notification_topic = sns.Topic(
            self,
            "DeploymentNotifications",
            display_name="Deployment Notifications",
            topic_name="deployment-notifications",
        )

        #1.1 Adding subscription to SNS topic for notifications
        self.notification_topic.add_subscription(
            subs.EmailSubscription(email)
        )        

        # ----------------------
        # 2. Creating human IAM roles below
        # ----------------------

        #2.1 Creating DevOps role for managing services after deployment
        self.devops_role = iam.Role(
            self,
            "DevOpsRole",
            assumed_by=iam.AccountRootPrincipal(), #ASSIGN TO IAM USER, GROUP, or SSO ROLES IN PROD
            role_name="DevOpsRole",
        )

        #2.1.1 Creating custom DevOps role permissions policy
        #Restrict below permissions once requirements are defined
        self.devops_role.add_to_policy(
            iam.PolicyStatement(
                actions=[ 
                    "cloudformation:*",
                    "iam:PassRole",
                    "s3:*",
                    "ec2:*",
                    "logs:*",
                    "sns:*"
                ],
                resources=["*"],  # Restrict later to resource ARNS in the account
            )
        )

        #2.2 Creating ReadOnly role for monitoring services after deployment
        self.read_only_role = iam.Role(
            self,
            "ReadOnlyRole",
            assumed_by=iam.AccountRootPrincipal(),  #ASSIGN TO IAM USER, GROUP, or SSO ROLES IN PROD
            role_name="ReadOnlyRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
            ],
        )        

        #3 Creating centralised CloudWatch log group location to aggregate logs related to the stack
        self.log_group = logs.LogGroup(
            self,
            "CoreLogGroup",
            log_group_name="/cdk/core-stack",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=RemovalPolicy.DESTROY #Set to RETAIN for prod.
        )

        #4 Creating CloudWatch metric filter to identify logs with 'ERROR' string
        self.error_metric = logs.MetricFilter(
            self,
            "ErrorMetricFilter",
            log_group=self.log_group,
            metric_namespace="LandingZone/Core",
            metric_name="ErrorCount",
            filter_pattern=logs.FilterPattern.literal("ERROR"),
            metric_value="1",
        )

        #5 Creating Cloudwatch alarm for the 'ERROR' string logs identified
        self.error_alarm = cw.Alarm(
            self,
            "ErrorAlarm",
            metric=self.error_metric.metric(),
            threshold=1,
            evaluation_periods=1,
            alarm_description="Alarm if an ERROR is detected in logs",
            alarm_name="LandingZoneErrorAlarm"
        )

        #5.1 If the alarm is triggerd (IN_ALARM), then a notification will be sent to the email address specified 
        self.error_alarm.add_alarm_action(cw_actions.SnsAction(self.notification_topic))

        #6 Output some of the resources deployed from this stack
        self.output_arns()
    
    def output_arns(self):
        CfnOutput(self, "SNSTopicARN", value=self.notification_topic.topic_arn)
        CfnOutput(self, "CloudWatchLogGroupName", value=self.log_group.log_group_name)
        CfnOutput(self, "DevOpsRoleARN", value=self.devops_role.role_arn)
        CfnOutput(self, "ReadOnlyRoleARN", value=self.read_only_role.role_arn)    


        
