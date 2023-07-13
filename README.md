# CDK CR (Custom Resource) Deoendency Issue

## the steps to reproduce inconsistent deletion

0. Set up Python and environment

```
curl -sSL https://install.python-poetry.org | python3 -
poetry shell
poetry install

curl -sL https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.bash_profile
npm install -g aws-cdk
```

1. Deploy

```
DEPLOY_AWS_ACCOUNT_ID=xxxxxxxxxxxx cdk deploy
```

2. Uncomment the line 50-57 in `main/main.py`

3. Deploy again

```
DEPLOY_AWS_ACCOUNT_ID=xxxxxxxxxxxx cdk deploy
```

4. Delete the stack to reproduce the issue

```
DEPLOY_AWS_ACCOUNT_ID=xxxxxxxxxxxx cdk destroy
```

5. You should see the Load Balancer and Custom Resource are being deleted at the same time. However, we should expect the Load Balancer is deleted before Custom Resource.
