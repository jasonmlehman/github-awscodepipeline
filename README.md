# Template AWS Cloud Development Kit (CDK) repository to use GitHub as a source repository for AWS Code Pipelines

1)  Update tags.json with any relevant tags for your project.

2)  Update CDK.json with the Account ID where the CodePipelines will be deployed to.

3)  Optionally update the Account ID where the infrascture will be deployed to.  This account will need a boostrap CDK trust with the codepipeline account