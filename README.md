Points:

- Roles separated by human vs service roles with least privilege principle applied.

Roles are currenty assumed by AccountRootPrincipal(). Following least privilege principle, for production, consider:

- Assigning the roles to specific IAM users, groups, or SSO roles.

- Narrowing 'DevOpsRole' (in [core_stack.py](stacks\core_stack.py)) service permissions as it currently uses service wildcards for demo purposes.

---

- Prod S3 Bucket removal policy currently set to DESTROY. For production, consider:

- Adjusting Prod S3 Bucket removal policy (in [prod_stack.py](stacks/prod_stack.py)) to RETAIN.

---

- CloudWatch Logs removal policy currently set to DESTROY. For production, consider:

- Adjusting CloudWatch Logs removal policy (in [core_stack.py](stacks/core_stack.py)) to RETAIN.

---

- Adjust [cdk-deploy.yml](.github/workflows/cdk-deploy.yml) environment variables accordingly.
- Add your AWS_ACCOUNT_ID as a GitHub Actions secret. This is required for the CI/CD workflow to run.
- Adjust [app.py](app.py) variables section accordingly.

---

Overview Diagram:

![Overview Diagram](images/cdk-landing-zone-overview.jpg)

Architecture Diagram:

