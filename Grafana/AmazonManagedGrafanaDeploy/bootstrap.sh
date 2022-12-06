#!/bin/sh
export PATH=/usr/local/bin:$PATH;

# Install docker and docker-compose
yum update
yum install docker jq -y
service docker start
usermod -a -G docker ec2-user
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
chown root:docker /usr/local/bin/docker-compose

# Update aws-cli
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install
pip3 install --upgrade --user awscli
echo 'export PATH=$HOME/.local/bin:$PATH' | tee -a ~/.bashrc && source ~/.bashrc

# Set default aws region
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region')
aws configure set default.region ${AWS_REGION}
aws configure get default.region

# Get grafana endpoint
export GRAFANA_URL=$(aws grafana list-workspaces | jq -r '.workspaces | .[] | select(.name == "AMG-WORKSPACE") | .endpoint')
export GRAFANA_ID=$(aws grafana list-workspaces | jq -r '.workspaces | .[] | select(.name == "AMG-WORKSPACE") | .id')
export KEYCLOAK_URL=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

# Create docker-compose file
cat <<EOF >/home/ec2-user/docker-compose.yml
version: '3'

volumes:
  postgres_data:
      driver: local

services:
  postgres:
      image: postgres
      container_name: postgres
      volumes:
        - postgres_data:/var/lib/postgresql/data
      environment:
        POSTGRES_DB: keycloak
        POSTGRES_USER: keycloak
        POSTGRES_PASSWORD: password
  keycloak:
      image: quay.io/keycloak/keycloak:legacy
      container_name: keycloak
      environment:
        DB_VENDOR: POSTGRES
        DB_ADDR: postgres
        DB_DATABASE: keycloak
        DB_USER: keycloak
        DB_SCHEMA: public
        DB_PASSWORD: password
        KEYCLOAK_USER: admin
        KEYCLOAK_PASSWORD: Pa55w0rd
        JDBC_PARAMS: "ssl=false"
      ports:
        - 80:8080
      depends_on:
        - postgres
EOF

chown ec2-user:ec2-user /home/ec2-user/docker-compose.yml
/usr/local/bin/docker-compose -f /home/ec2-user/docker-compose.yml up -d

cat << EOF > configure.sh
./opt/jboss/keycloak/bin/kcadm.sh config credentials \
    --server http://localhost:8080/auth \
    --realm master \
    --user admin \
    --password Pa55w0rd

./opt/jboss/keycloak/bin/kcadm.sh update realms/master -s sslRequired=NONE
./opt/jboss/keycloak/bin/kcadm.sh create realms -f - << END
{
    "realm": "eksdemo",
    "enabled": true,
    "roles": {
    "realm": [
        {
        "name": "admin"
        }
    ]
    },
    "sslRequired": "none",
    "users": [
    {
        "username": "admin",
        "email": "admin@eksdemo",
        "enabled": true,
        "firstName": "Admin",
        "realmRoles": [
        "admin"
        ],
        "credentials": [
        {
            "type": "password",
            "value": "Pa55w0rd"
        }
        ]
    }
    ],
    "clients": [
    {
        "clientId": "https://${GRAFANA_URL}/saml/metadata",
        "name": "amazon-managed-grafana",
        "enabled": true,
        "protocol": "saml",
        "adminUrl": "https://${GRAFANA_URL}/login/saml",
        "redirectUris": [
        "https://${GRAFANA_URL}/saml/acs"
        ],
        "attributes": {
        "saml.authnstatement": "true",
        "saml.server.signature": "true",
        "saml_name_id_format": "email",
        "saml_force_name_id_format": "true",
        "saml.assertion.signature": "true",
        "saml.client.signature": "false"
        },
        "defaultClientScopes": [],
        "protocolMappers": [
        {
            "name": "name",
            "protocol": "saml",
            "protocolMapper": "saml-user-property-mapper",
            "consentRequired": false,
            "config": {
            "attribute.nameformat": "Unspecified",
            "user.attribute": "firstName",
            "attribute.name": "displayName"
            }
        },
        {
            "name": "email",
            "protocol": "saml",
            "protocolMapper": "saml-user-property-mapper",
            "consentRequired": false,
            "config": {
            "attribute.nameformat": "Unspecified",
            "user.attribute": "email",
            "attribute.name": "mail"
            }
        },
        {
            "name": "role list",
            "protocol": "saml",
            "protocolMapper": "saml-role-list-mapper",
            "config": {
            "single": "true",
            "attribute.nameformat": "Unspecified",
            "attribute.name": "role"
            }
        }
        ]
    }
    ]
}
END
EOF

sleep 75
docker exec  -i  keycloak  /bin/sh  <  configure.sh

aws grafana update-workspace-authentication \
    --workspace-id ${GRAFANA_ID} \
    --authentication-providers '["SAML"]' \
    --saml-configuration "{\"idpMetadata\": {\"url\": \"http://${KEYCLOAK_URL}/auth/realms/eksdemo/protocol/saml/descriptor\"}, \"assertionAttributes\": {\"role\": \"role\"}, \"roleValues\": {\"admin\": [\"admin\"]}}"